<template>
    <div>
        <div id="map"></div>
        <b-sidebar id="sidebar-left" title="Меню" :visible="isSidebarVisible" :backdrop="true"
            @hidden="isSidebarVisible = false" bg-variant="light" text-variant="dark" left>
            <div>
                <p>{{ this.sidebarData }}</p>
                <b-button variant="danger" @click="closeSidebar">Закрыть</b-button>
            </div>
        </b-sidebar>
    </div>
</template>

<script>
/* eslint-disable */
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import * as turf from 'turf';

export default {
    data() {
        return {
            socketgetplane: null,
            map: null,
            startCoordinates: [24.7, 56.9],
            planeCollection: {},
            isSidebarVisible: false,
            sidebarCallSign: null,
            sidebarData: null,
            fetchInterval: null,
        };
    },
    mounted() {
        this.map = new maplibregl.Map({
            container: 'map',
            style: 'https://tiles.openfreemap.org/styles/liberty',
            center: this.startCoordinates,
            zoom: 6.5,
        });

        this.map.on('click', (e) => {
            const features = this.map.queryRenderedFeatures(e.point, {
                layers: [this.layerId],
            });

            if (!features.length) {
                // Удалить маршрут, если кликнули на пустую область
                if (this.map.getSource('route')) {
                    this.map.removeLayer('route-layer');
                    this.map.removeSource('route');
                }

                // Сбросить выбор всех самолетов
                Object.values(this.planeCollection).forEach((plane) => {
                    plane.isChoosed = false;
                });
            }
        });

    },
    created() {
        this.setupWebSocketPlanes();
    },
    methods: {
        removePlaneFromCollection(callSign) {
            this.$delete(this.planeCollection, callSign);
        },

        addPlaneToCollection(callSign, plane) {
            this.$set(this.planeCollection, callSign, plane);
        },

        setupWebSocketPlanes() {
            this.socketgetplane = new WebSocket('ws://localhost:8082');

            this.socketgetplane.onopen = () => {
                console.log('WebSocketGetPlane connected');
            };

            this.socketgetplane.onmessage = (event) => {
                console.log('--------------------------------');
                const data = JSON.parse(event.data);
                console.log('Received plane:', data);
                const position = [data.Position_latitude, data.Position_longitude];

                if (this.planeCollection[data.Callsign]) {
                    console.log(`Plane with callSign ${data.Callsign} already exists.`);
                    this.planeCollection[data.Callsign].updatePosition(data.Position_longitude, data.Position_latitude, data.direction);
                } else {
                    this.planeCollection[data.Callsign] = new Plane(
                        data.Position_longitude,
                        data.Position_latitude,
                        data.Callsign,
                        data.direction,
                        this.map,
                        this.removePlaneFromCollection,
                        this.toggleSidebar,
                    );
                    console.log(`Plane ${data.Callsign} added to collection.`);
                }
            };

            this.socketgetplane.onerror = (error) => {
                console.error('WebSocketGetPlane error:', error);
            };
        },

        toggleSidebar(callSign) {
            this.isSidebarVisible = true;
            this.sidebarCallSign = callSign;
            this.fetchSidebarData();

            if (this.fetchInterval) clearInterval(this.fetchInterval);

            // Установить интервал для обновления данных раз в секунду
            this.fetchInterval = setInterval(this.fetchSidebarData, 1000);
        },

        closeSidebar() {
            this.isSidebarVisible = false;
            this.sidebarCallSign = null;
            this.sidebarData = null;

            // Остановить запросы, если сайдбар закрыт
            if (this.fetchInterval) clearInterval(this.fetchInterval);
            this.fetchInterval = null;
        },

        async fetchSidebarData() {
            if (!this.sidebarCallSign) return;

            try {
                const response = await fetch(`http://localhost:8000/api/plane/${this.sidebarCallSign}/`);
                if (!response.ok) throw new Error('Ошибка загрузки данных');
                const data = await response.json();
                this.sidebarData = JSON.stringify(data, null, 2); // Форматируем JSON для отображения
            } catch (error) {
                console.error('Ошибка при запросе данных:', error);
                this.sidebarData = 'Не удалось загрузить данные';
            }
        },
    },
};

class Plane {
    constructor(longitude, latitude, callSign, rotation, map, removePlaneFromCollection, toggleSidebar) {
        this.longitude = longitude;
        this.latitude = latitude;
        this.rotation = rotation;
        this.callSign = callSign;
        this.sourceId = `plane-source-${callSign}`;
        this.layerId = `plane-layer-${callSign}`;
        this.map = map;
        this.deleteAfterSeconds = 15000;
        this.timer = null;
        this.removePlaneFromCollection = removePlaneFromCollection;
        this.toggleSidebar = toggleSidebar;
        this.previousPositions = [];
        this.routeSourceId = 'route'; // Имя источника маршрута
        this.routeLayerId = 'route-layer'; // Имя слоя маршрута
        this.isChoosed = false;

        console.log(`${this.callSign} plane has been created.`);

        const width = 8;
        const bytesPerPixel = 4;
        const data = new Uint8Array(width * width * bytesPerPixel);

        for (let x = 0; x < width; x++) {
            for (let y = 0; y < width; y++) {
                const offset = (y * width + x) * bytesPerPixel;
                data[offset + 0] = (y / width) * 255;
                data[offset + 1] = (x / width) * 255;
                data[offset + 2] = 128;
                data[offset + 3] = 255;
            }
        }

        this.map.addImage(`plane-${callSign}`, { width, height: width, data });

        this.map.addSource(this.sourceId, {
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: [
                    {
                        type: 'Feature',
                        geometry: {
                            type: 'Point',
                            coordinates: [this.longitude, this.latitude],
                        },
                        properties: {
                            rotation: this.rotation,
                        },
                    },
                ],
            },
        });

        this.map.addLayer({
            id: this.layerId,
            type: 'symbol',
            source: this.sourceId,
            layout: {
                'icon-image': `plane-${callSign}`,
                'icon-rotate': ['get', 'rotation'],
                'icon-size': 1.5,
            },
        });

        this.map.on('click', this.layerId, (e) => {
            this.isChoosed = true;
            this.showRoute();
            this.toggleSidebar(this.callSign);
        });

        this.startDeleteTimer();
    }

    showRoute() {
        // Удалить предыдущий маршрут, если он существует
        if (this.map.getSource(this.routeSourceId)) {
            this.map.removeLayer(this.routeLayerId);
            this.map.removeSource(this.routeSourceId);
        }

        // Создать новый маршрут
        this.route = {
            type: 'FeatureCollection',
            features: [
                {
                    type: 'Feature',
                    geometry: {
                        type: 'LineString',
                        coordinates: this.previousPositions,
                    },
                },
            ],
        };

        this.map.addSource(this.routeSourceId, {
            type: 'geojson',
            data: this.route,
        });

        this.map.addLayer({
            id: this.routeLayerId,
            type: 'line',
            source: this.routeSourceId,
            layout: {
                'line-join': 'round',
                'line-cap': 'round',
            },
            paint: {
                'line-color': '#FF5733',
                'line-width': 4,
            },
        });


    }

    updatePosition(newLongitude, newLatitude, newRotation) {
        this.longitude = newLongitude;
        this.latitude = newLatitude;
        this.rotation = newRotation;

        // Добавить текущую позицию в массив previousPositions
        this.previousPositions.push([this.longitude, this.latitude]);

        if (this.map.getSource(this.sourceId)) {
            this.map.getSource(this.sourceId).setData({
                type: 'FeatureCollection',
                features: [
                    {
                        type: 'Feature',
                        geometry: {
                            type: 'Point',
                            coordinates: [this.longitude, this.latitude],
                        },
                        properties: {
                            rotation: this.rotation,
                        },
                    },
                ],
            });
        }

        if (this.isChoosed) {
            if (this.map.getSource(this.routeSourceId)) {
                // Дополнить маршрут новыми координатами
                const routeData = this.map.getSource(this.routeSourceId)._data;
                routeData.features[0].geometry.coordinates.push([this.longitude, this.latitude]);

                // Обновить источник маршрута
                this.map.getSource(this.routeSourceId).setData(routeData);
            } else {
                // Если маршрут еще не создан, создать его
                this.showRoute();
            }
        }

        this.resetDeleteTimer();
    }




    startDeleteTimer() {
        // this.timer = setTimeout(() => {
        //     console.log(`${this.callSign} not updated, removing from collection.`);
        //     this.destroy();
        // }, this.deleteAfterSeconds);
    }

    resetDeleteTimer() {
        // if (this.timer) {
        //     clearTimeout(this.timer);
        // }
        // this.startDeleteTimer();
    }

    destroy() {
        // console.log(`${this.callSign} is being destroyed.`);
        // if (this.map.getLayer(this.layerId)) {
        //     this.map.removeLayer(this.layerId);
        // }
        // if (this.map.getSource(this.sourceId)) {
        //     this.map.removeSource(this.sourceId);
        // }
        // if (this.map.getSource(this.routeSourceId)) {
        //     this.map.removeLayer(this.routeLayerId);
        //     this.map.removeSource(this.routeSourceId);
        // }

        // // Сбросить флаг выбора
        // this.isChoosed = false;

        // // Удалить самолет из коллекции
        // this.removePlaneFromCollection(this.callSign);
    }
}

</script>

<style scoped>
#map {
    position: absolute;
    top: 112px;
    left: 0;
    width: 100%;
    height: calc(100% - 112px);
}
</style>