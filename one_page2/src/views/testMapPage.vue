<template>
    <div>
        <div id="map"></div>
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
        };
    },
    mounted() {
        this.map = new maplibregl.Map({
            container: 'map',
            style: 'https://tiles.openfreemap.org/styles/liberty',
            center: this.startCoordinates,
            zoom: 6.5,
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
                    // Создаём новый объект Plane и добавляем в коллекцию
                    this.planeCollection[data.Callsign] = new Plane(
                        data.Position_longitude,
                        data.Position_latitude,
                        data.Callsign,
                        data.direction,
                        this.map,
                        this.removePlaneFromCollection,
                    );
                    console.log(`Plane ${data.Callsign} added to collection.`);
                }
            };

            this.socketgetplane.onerror = (error) => {
                console.error('WebSocketGetPlane error:', error);
            };
        },
    },
};

class Plane {
    constructor(longitude, latitude, callSign, rotation, map, removePlaneFromCollection) {
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

        console.log(`${this.callSign} plane has been created.`);

        //-------------------------------------------------------------------------------------------------------------------
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

        this.startDeleteTimer();
    }

    updatePosition(newLongitude, newLatitude, newRotation) {
        this.longitude = newLongitude;
        this.latitude = newLatitude;
        this.rotation = newRotation;

        if (!this.map.getLayer(this.layerId)) {
            this.map.addLayer({
                id: this.layerId,
                type: 'symbol',
                source: this.sourceId,
                layout: {
                    'icon-image': `plane-${this.callSign}`,
                    'icon-rotate': ['get', 'rotation'],
                    'icon-size': 1.5,
                },
            });
        }

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

        this.map.on('click', this.layerId, (e) => {
            const features = this.map.queryRenderedFeatures(e.point, {
                layers: [this.layerId]
            });

            if (features.length > 0) {
                const feature = features[0];
                // Выводим сообщение при клике
                console.log(`You clicked on plane with call sign: ${this.callSign}`);
            }
        });
        //------------------------------------------------------------------------------------------------------
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