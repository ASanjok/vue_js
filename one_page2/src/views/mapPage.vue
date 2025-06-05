<template>
    <div>
        <div id="map"></div>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow
            :visible="isSidebarVisible" :backdrop="false" @hidden="isSidebarVisible = false" bg-variant="light"
            text-variant="dark" left style="width: 180px;">
            <template v-if="localSidebarData.length">
                <b-card class="mb-2" header="header" header-bg-variant="primary" header-text-variant="white">

                    <draggable v-model="localSidebarData">
                        <transition-group name="flip-list" tag="ul">
                            <li v-for="(item) in localSidebarData" :key="item.key" class="list-group-item py-1 px-2"
                                style="cursor: move; list-style: none;">
                                <strong>{{ item.key }}</strong>: {{ item.value }}
                            </li>
                        </transition-group>
                    </draggable>

                </b-card>
            </template>

            <template v-else>
                <b-alert variant="info" show>
                    Loading...
                </b-alert>
            </template>
        </b-sidebar>
    </div>
</template>


<script>
/* eslint-disable */
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import axios from 'axios';
import draggable from 'vuedraggable';

export default {
    components: { draggable },
    props: ['sidebarData'],
    data() {
        return {
            localSidebarData: [],
            socketgetplane: null,
            map: null,
            startCoordinates: [24.7, 56.9],
            planeCollection: {},
            isSidebarVisible: false,
            sidebarCallSign: null,
            tableFields: [
                { key: 'key', label: 'Parameter' },
                { key: 'value', label: 'Value' },
            ],
        };
    },
    watch: {
        '$store.state.choosedCallSign'(newCallSign) {
            if (newCallSign && this.planeCollection[newCallSign]) {
                this.planeCollection[newCallSign].select();
            }
        },
        sidebarData: {
            handler(newVal) {
                if (!newVal || Object.keys(newVal).length === 0) return;

                const existingKeys = this.localSidebarData.map(i => i.key);
                const newKeys = Object.keys(newVal);

                const updatedData = [];

                for (const key of existingKeys) {
                    if (newKeys.includes(key)) {
                        updatedData.push({
                            key,
                            value: newVal[key]
                        });
                    }
                }

                for (const key of newKeys) {
                    if (!existingKeys.includes(key)) {
                        updatedData.push({
                            key,
                            value: newVal[key]
                        });
                    }
                }

                this.localSidebarData = updatedData;
            },
            immediate: true,
            deep: true
        }
    },
    mounted() {
        this.map = new maplibregl.Map({
            container: 'map',
            style: 'https://tiles.openfreemap.org/styles/liberty',
            center: this.startCoordinates,
            zoom: 6.5,
        });

        this.map.on('click', (e) => {
            const features = this.map.queryRenderedFeatures(e.point);

            if (!features.length) {
                const layers = this.map.getStyle().layers;
                const sources = this.map.getStyle().sources;

                layers.forEach(layer => {
                    if (layer.id.startsWith('route-layer-')) {
                        this.map.removeLayer(layer.id);
                    }
                });

                Object.keys(sources).forEach(sourceId => {
                    if (sourceId.startsWith('route-')) {
                        this.map.removeSource(sourceId);
                    }
                });

                Object.values(this.planeCollection).forEach((plane) => {
                    plane.isChoosed = false;
                });

                this.toggleSidebar();
            }
        });
    },
    created() {
        this.setupWebSocketPlanes();
    },
    beforeDestroy() {
        if (this.socketgetplane) {
            this.socketgetplane.close();
            console.log("WebSocketGetPlane закрыт.");
        }
    },
    onBeforeUnmount() {
        if (this.socketgetplane) {
            this.socketgetplane.close();
            console.log("WebSocketGetPlane закрыт.");
        }
    },
    methods: {
        onDragEnd() {
            console.log("New order:", this.localSidebarData);
        },
        async refreshToken() {
            try {
                const refreshToken = localStorage.getItem('refreshToken');
                console.log("refresh token used - ", refreshToken)
                if (refreshToken) {
                    const response = await axios.post('http://localhost:8000/api/token/refresh/', {
                        refresh: refreshToken,
                    });

                    if (response.data.access) {
                        localStorage.setItem('authToken', response.data.access);
                        console.log('Token refreshed successfully, new access token - ', response.data.access);
                    }
                }
            } catch (error) {
                console.error('Failed to refresh token:', error);
            }
        },
        removePlaneFromCollection(callSign) {
            this.$delete(this.planeCollection, callSign);

            this.$store.commit('setPlanesCallSigns', this.planeCollection)
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

                if (this.planeCollection[data.Callsign]) {
                    console.log(`Plane with callSign ${data.Callsign} already exists.`);
                    this.planeCollection[data.Callsign].updatePosition(data);
                } else {
                    this.planeCollection[data.Callsign] = new Plane(
                        data.Position_longitude,
                        data.Position_latitude,
                        data.Callsign,
                        data.Track,
                        this.map,
                        this.removePlaneFromCollection,
                        this.toggleSidebar,
                    );
                    this.$store.commit('setPlanesCallSigns', this.planeCollection)
                    console.log(`Plane ${data.Callsign} added to collection.`);


                }
                if (this.isSidebarVisible && this.sidebarCallSign === data.Callsign) {
                    this.sidebarData = data;
                }
            };

            this.socketgetplane.onerror = (error) => {
                console.error('WebSocketGetPlane error:', error);
            };
        },
        toggleSidebar(CallSign = null) {
            this.refreshToken();
            if (CallSign == null) {
                this.isSidebarVisible = false;
                this.sidebarCallSign = null;
                this.sidebarData = {};
            } else {
                this.isSidebarVisible = true;
                this.sidebarCallSign = CallSign;

                console.log("sidebar open )))))", this.planeCollection[CallSign])
                if (this.planeCollection[CallSign]) {
                    this.sidebarData = { longitude: this.planeCollection[CallSign].longitude, latitude: this.planeCollection[CallSign].latitude, callSign: this.planeCollection[CallSign].callSign }
                    console.log("((()))", this.sidebarData)
                }
            }
        },
    }
};

class Plane {
    constructor(longitude, latitude, callSign, rotation, map, removePlaneFromCollection, toggleSidebar, sidebardata) {
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
        this.routeSourceId = `route-${callSign}`; 
        this.routeLayerId = `route-layer-${callSign}`; 
        this.isChoosed = false;
        this.sidebarData = sidebardata;

        console.log(`${this.callSign} plane has been created.`);

        const width = 16;  
        const height = 16; 
        const bytesPerPixel = 4;
        const data = new Uint8Array(width * height * bytesPerPixel);

        const triangleColor = [255, 100, 50, 255]; 

        const centerX = width / 2;
        const baseY = height - 1;
        const peakY = 2; 

        const baseWidthFactor = 0.3;

        for (let y = peakY; y <= baseY; y++) {
            let halfWidth = ((y - peakY) / (baseY - peakY)) * (width * baseWidthFactor); 
            let leftX = Math.floor(centerX - halfWidth);
            let rightX = Math.ceil(centerX + halfWidth);

            for (let x = leftX; x <= rightX; x++) {
                const offset = (y * width + x) * bytesPerPixel;
                data[offset + 0] = triangleColor[0]; 
                data[offset + 1] = triangleColor[1]; 
                data[offset + 2] = triangleColor[2]; 
                data[offset + 3] = triangleColor[3]; 
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
        },);

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
            this.select()
        });

        this.startDeleteTimer();
    };

    select() {
        this.isChoosed = true;
        this.showRoute();
        this.hideRoute();
        this.toggleSidebar(this.callSign);
    };

    async showRoute() {
        if (this.map.getSource(this.routeSourceId)) {
            this.map.removeLayer(this.routeLayerId);
            this.map.removeSource(this.routeSourceId);
        }

        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch(`http://localhost:8000/api/previousePositions/${this.callSign}/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Ошибка загрузки данных');
            }

            const positions = await response.json();
            console.log("\n\nПолученные позиции:\n", positions);

            const coordinates = positions.positions.map(pos => {
                const wkt = pos.position; 
                const match = wkt.match(/POINT\s?\(([-\d.]+)\s+([-\d.]+)\)/);
                if (match) {
                    const longitude = parseFloat(match[1]);
                    const latitude = parseFloat(match[2]);
                    return [longitude, latitude];
                }
                return null; 
            }).filter(coord => coord !== null); 

            if (coordinates.length === 0) {
                console.error("Нет координат для отображения маршрута.");
                return;
            }

            this.map.addSource(this.routeSourceId, {
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: [
                        {
                            type: 'Feature',
                            geometry: {
                                type: 'LineString',
                                coordinates: coordinates,
                            },
                        },
                    ],
                },
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

            console.log("Маршрут успешно отображён.");
        } catch (error) {
            console.error(`Ошибка загрузки маршрута для ${this.callSign}:`, error);
        }
    }

    hideRoute() {
        const layers = this.map.getStyle().layers;
        const sources = this.map.getStyle().sources;

        layers.forEach(layer => {
            if (layer.id.startsWith('route-layer-')) {
                this.map.removeLayer(layer.id);
            }
        });

        Object.keys(sources).forEach(sourceId => {
            if (sourceId.startsWith('route-')) {
                this.map.removeSource(sourceId);
            }
        });

        console.log("Удалены все маршруты.");
    }

    updatePosition(data) {
        this.longitude = data.Position_longitude;
        this.latitude = data.Position_latitude;
        this.rotation = data.Track;

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
                const routeData = this.map.getSource(this.routeSourceId)._data;
                routeData.features[0].geometry.coordinates.push([this.longitude, this.latitude]);

                this.map.getSource(this.routeSourceId).setData(routeData);
            }
        }
        this.sidebarData = data;

        this.resetDeleteTimer();
    }

    startDeleteTimer() {
        this.timer = setTimeout(() => {
            console.log(`${this.callSign} not updated, removing from collection.`);
            this.destroy();
        }, this.deleteAfterSeconds);
    }

    resetDeleteTimer() {
        if (this.timer) {
            clearTimeout(this.timer);
        }
        this.startDeleteTimer();
    }

    destroy() {
        console.log(`${this.callSign} is being destroyed.`);
        if (this.map.getLayer(this.layerId)) {
            this.map.removeLayer(this.layerId);
        }
        if (this.map.getSource(this.sourceId)) {
            this.map.removeSource(this.sourceId);
        }
        if (this.map.getSource(this.routeSourceId)) {
            this.map.removeLayer(this.routeLayerId);
            this.map.removeSource(this.routeSourceId);
        }

        this.isChoosed = false;

        this.removePlaneFromCollection(this.callSign);
    }
}
</script>

<style scoped>
#map {
    position: absolute;
    top: 56px;
    left: 0;
    width: 100%;
    height: calc(100% - 56px);
}

:deep(.b-sidebar) {
    width: fit-content;
    min-width: 33vw;
}

.flip-list-move {
    transition: transform 0.3s ease;
}
</style>