<template>
    <div>
        <!-- Main map container -->
        <div id="map"></div>

        <!-- Sidebar displaying additional flight data -->
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow
            :visible="isSidebarVisible" :backdrop="false" @hidden="isSidebarVisible = false" bg-variant="light"
            text-variant="dark" left style="width: 180px;">
            <!-- If there is data, display it in a draggable list -->
            <template v-if="localSidebarData.length">
                <b-card class="mb-2" header="header" header-bg-variant="primary" header-text-variant="white">
                    <!-- Draggable list of key-value pairs -->
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

            <!-- Show loading message if no data -->
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
    components: {
        draggable  // Enables drag-and-drop functionality inside the sidebar
    },
    props: ['sidebarData'],  // Receives flight data for the sidebar as a prop
    data() {
        return {
            localSidebarData: [],          // Local copy of sidebar data for display and manipulation
            socketgetplane: null,          // WebSocket connection for receiving live plane data
            map: null,                     // MapLibre map instance
            startCoordinates: [24.7, 56.9], // Initial map center (Riga, Latvia)
            planeCollection: {},           // Stores all plane markers and related data
            isSidebarVisible: false,       // Controls sidebar visibility
            sidebarCallSign: null,         // Currently selected callsign (plane identifier)
            tableFields: [                 // Table layout structure for displaying key-value pairs
                { key: 'key', label: 'Parameter' },
                { key: 'value', label: 'Value' },
            ],
        };
    },
    watch: {
        '$store.state.mapStyle'(newStyle) {
            if (this.map) {
                const newStyleUrl = `https://tiles.openfreemap.org/styles/${newStyle}`;
                this.map.setStyle(newStyleUrl);
                console.log('Map style changed to:', newStyleUrl);
                this.planeCollection = {};
            }
        },
        // Watcher for changes in selected callsign from Vuex store
        '$store.state.choosedCallSign'(newCallSign) {
            if (newCallSign && this.planeCollection[newCallSign]) {
                // If the selected plane exists, trigger its highlight/select logic
                this.planeCollection[newCallSign].select();
            }
        },
        // Watcher for incoming sidebar data updates
        sidebarData: {
            handler(newVal) {
                if (!newVal || Object.keys(newVal).length === 0) return;

                const keyLabelMap = {
                    Speed: 'Speed (km/h)',
                    Track: 'Track (°)',
                    Altitude: 'Altitude (km)',
                    Position_latitude: 'Latitude',
                    Position_longitude: 'Longitude',
                    RC: 'Radius of Containment (RC)',
                    EPU: 'Estimated Position Uncertainty (EPU)',
                    ICAO: 'ICAO ID',
                    VEPU: 'Vertical EPU',
                    HFOMr: 'Horizontal Figure of Merit',
                    VFOMr: 'Vertical Figure of Merit',
                    Callsign: 'Call Sign',
                    PlaceName: 'Location',
                    PlaneDistance: 'Distance to Location (km)',
                    TimeReceived: 'Time Received',
                };

                const existingKeys = this.localSidebarData.map(i => i.key);
                const updatedData = [];

                // Format date as "5 February 2025, 19:25"
                const formatDate = (value) => {
                    const date = new Date(value);
                    return isNaN(date) ? value : date.toLocaleString('en-GB', {
                        day: 'numeric',
                        month: 'long',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit',
                        hour12: false
                    });
                };

                // Format numeric values to 2 decimals
                const toFixed = (val, decimals = 2) => Number.parseFloat(val).toFixed(decimals);

                // Update existing keys preserving order
                for (const item of this.localSidebarData) {
                    const rawKey = Object.keys(keyLabelMap).find(k => keyLabelMap[k] === item.key);
                    let value = newVal[rawKey];

                    if (value !== undefined) {
                        switch (rawKey) {
                            case 'Altitude':
                                value = `${toFixed(value / 1000, 2)} km`;
                                break;
                            case 'PlaneDistance':
                                value = `${toFixed(value, 2)} km`;
                                break;
                            case 'Speed':
                                value = `${toFixed(value * 1.852, 1)} km/h`;
                                break;
                            case 'Track':
                                value = toFixed(value, 0);
                                break;
                            case 'Position_latitude':
                            case 'Position_longitude':
                                value = toFixed(value, 2);
                                break;
                            case 'MlatTime':
                            case 'TimeReceived':
                                value = formatDate(value);
                                break;
                        }
                        updatedData.push({ key: item.key, value });
                    } else {
                        updatedData.push(item); // Keep the current one if no new value
                    }
                }

                // Add any new keys not in localSidebarData yet
                for (const rawKey of Object.keys(newVal)) {
                    const label = keyLabelMap[rawKey];
                    if (label && !existingKeys.includes(label)) {
                        let value = newVal[rawKey];

                        switch (rawKey) {
                            case 'Altitude':
                                value = `${toFixed(value / 1000, 3)} km`;
                                break;
                            case 'PlaneDistance':
                                value = `${toFixed(value, 2)} km`;
                                break;
                            case 'Speed':
                                value = `${toFixed(value * 1.852, 1)} km/h`;
                                break;
                            case 'Track':
                            case 'Position_latitude':
                            case 'Position_longitude':
                                value = toFixed(value, 2);
                                break;
                            case 'MlatTime':
                            case 'TimeReceived':
                                value = formatDate(value);
                                break;
                        }

                        updatedData.push({ key: label, value });
                    }
                }

                this.localSidebarData = updatedData;
            },
            immediate: true,
            deep: true
        }
    },
    mounted() {
        // Initialize the MapLibre map
        this.map = new maplibregl.Map({
            container: 'map', // HTML container ID for the map
            style: `https://tiles.openfreemap.org/styles/${this.$store.getters.mapStyle}`, // Tile style URL
            center: this.startCoordinates, // Initial center coordinates
            zoom: 6.5, // Initial zoom level
        });

        // Event handler for map clicks
        this.map.on('click', (e) => {
            // Get all features under the clicked point
            const features = this.map.queryRenderedFeatures(e.point);

            // If the user clicked on empty space
            if (!features.length) {
                const layers = this.map.getStyle().layers;
                const sources = this.map.getStyle().sources;

                // Remove all route-related layers
                layers.forEach(layer => {
                    if (layer.id.startsWith('route-layer-')) {
                        this.map.removeLayer(layer.id);
                    }
                });

                // Remove all route-related sources
                Object.keys(sources).forEach(sourceId => {
                    if (sourceId.startsWith('route-')) {
                        this.map.removeSource(sourceId);
                    }
                });

                // Deselect all planes
                Object.values(this.planeCollection).forEach((plane) => {
                    plane.isChoosed = false;
                });

                // Toggle sidebar visibility
                this.toggleSidebar();
            }
        });
    },
    created() {
        // Set up the WebSocket connection for receiving live plane data
        this.setupWebSocketPlanes();
    },
    beforeDestroy() {
        // Close WebSocket connection when component is about to be destroyed
        if (this.socketgetplane) {
            this.socketgetplane.close();
            console.log("WebSocketGetPlane closed.");
        }
    },
    onBeforeUnmount() {
        if (this.socketgetplane) {
            this.socketgetplane.close();
            console.log("WebSocketGetPlane closed.");
        }
    },
    methods: {
        // Called when the drag-and-drop operation ends
        onDragEnd() {
            console.log("New order:", this.localSidebarData);
        },

        // Refresh the JWT access token using the stored refresh token
        async refreshToken() {
            try {
                const refreshToken = localStorage.getItem('refreshToken');
                console.log("refresh token used - ", refreshToken);
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

        // Remove a plane from the plane collection by its call sign
        removePlaneFromCollection(callSign) {
            this.$delete(this.planeCollection, callSign);
            this.$store.commit('setPlanesCallSigns', this.planeCollection);
        },

        // Set up a WebSocket connection to receive live plane data
        setupWebSocketPlanes() {
            this.socketgetplane = new WebSocket('ws://localhost:8082');

            this.socketgetplane.onopen = () => {
                console.log('WebSocketGetPlane connected');
            };

            // When a message (plane data) is received from the server
            this.socketgetplane.onmessage = (event) => {
                console.log('--------------------------------');
                const data = JSON.parse(event.data);
                console.log('Received plane:', data);

                // If plane already exists in the collection, update its position
                if (this.planeCollection[data.Callsign]) {
                    console.log(`Plane with callSign ${data.Callsign} already exists.`);
                    this.planeCollection[data.Callsign].updatePosition(data);
                } else {
                    // If not, create a new plane and add it to the collection
                    this.planeCollection[data.Callsign] = new Plane(
                        data.Position_longitude,
                        data.Position_latitude,
                        data.Callsign,
                        data.Track,
                        this.map,
                        this.removePlaneFromCollection,
                        this.toggleSidebar,
                    );
                    this.$store.commit('setPlanesCallSigns', this.planeCollection);
                    console.log(`Plane ${data.Callsign} added to collection.`);
                }

                // Update sidebar data if it is currently showing this plane
                if (this.isSidebarVisible && this.sidebarCallSign === data.Callsign) {
                    this.sidebarData = data;
                }
            };

            // Handle WebSocket errors
            this.socketgetplane.onerror = (error) => {
                console.error('WebSocketGetPlane error:', error);
            };
        },

        // Show or hide the sidebar with plane details
        toggleSidebar(CallSign = null) {
            this.refreshToken(); // Refresh token each time sidebar is toggled

            if (CallSign == null) {
                // Hide sidebar and reset data
                this.isSidebarVisible = false;
                this.sidebarCallSign = null;
                this.sidebarData = {};
            } else {
                // Show sidebar and populate data for selected plane
                this.isSidebarVisible = true;
                this.sidebarCallSign = CallSign;

                console.log("sidebar open )))))", this.planeCollection[CallSign]);
                if (this.planeCollection[CallSign]) {
                    this.sidebarData = {
                        longitude: this.planeCollection[CallSign].longitude,
                        latitude: this.planeCollection[CallSign].latitude,
                        callSign: this.planeCollection[CallSign].callSign,
                    };
                    console.log("((()))", this.sidebarData);
                }
            }
        },
    }
};

class Plane {
    constructor(longitude, latitude, callSign, rotation, map, removePlaneFromCollection, toggleSidebar, sidebardata) {
        // Initial position and data
        this.longitude = longitude;
        this.latitude = latitude;
        this.rotation = rotation;
        this.callSign = callSign;

        // Unique identifiers for map source/layer
        this.sourceId = `plane-source-${callSign}`;
        this.layerId = `plane-layer-${callSign}`;

        this.map = map;

        // How long to wait (ms) before removing a plane if not updated
        this.deleteAfterSeconds = 15000;
        this.timer = null;

        this.removePlaneFromCollection = removePlaneFromCollection;
        this.toggleSidebar = toggleSidebar;
        this.previousPositions = [];

        // For route tracking (polyline)
        this.routeSourceId = `route-${callSign}`;
        this.routeLayerId = `route-layer-${callSign}`;
        this.isChoosed = false;
        this.sidebarData = sidebardata;

        console.log(`${this.callSign} plane has been created.`);

        // Draw the plane icon as a triangle on a small canvas
        const width = 16;
        const height = 16;
        const bytesPerPixel = 4;
        const data = new Uint8Array(width * height * bytesPerPixel);
        const triangleColor = [255, 100, 50, 255]; // RGBA

        const centerX = width / 2;
        const baseY = height - 1;
        const peakY = 2;
        const baseWidthFactor = 0.3;

        // Create triangle shape pixel by pixel
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

        // Add plane icon and data source to the map
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

        // Set up click handler for selecting this plane
        this.map.on('click', this.layerId, (e) => {
            this.select();
        });

        // Start the self-destruction timer if not updated
        this.startDeleteTimer();
    }

    // Called when the plane is clicked
    select() {
        this.isChoosed = true;
        this.showRoute();   // Show previous route
        this.toggleSidebar(this.callSign); // Open sidebar
    }

    // Load and draw route of previous positions from the backend
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
                throw new Error('Error loading route data');
            }

            const positions = await response.json();
            console.log("\n\nReceived positions:\n", positions);

            // Parse WKT POINT format
            const coordinates = positions.positions.map(pos => {
                const wkt = pos.position;
                const match = wkt.match(/POINT\s?\(([-\d.]+)\s+([-\d.]+)\)/);
                if (match) {
                    return [parseFloat(match[1]), parseFloat(match[2])];
                }
                return null;
            }).filter(coord => coord !== null);

            if (coordinates.length === 0) {
                console.error("No coordinates to display route.");
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

            console.log("Route displayed successfully.");
        } catch (error) {
            console.error(`Error loading route for ${this.callSign}:`, error);
        }
    }

    // Remove all route layers and sources from the map
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

        console.log("All routes removed.");
    }

    // Update plane's position and optionally extend its route
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

        // Add point to route if selected
        if (this.isChoosed && this.map.getSource(this.routeSourceId)) {
            const routeData = this.map.getSource(this.routeSourceId)._data;
            routeData.features[0].geometry.coordinates.push([this.longitude, this.latitude]);
            this.map.getSource(this.routeSourceId).setData(routeData);
        }

        // Update sidebar
        this.sidebarData = data;

        // Restart delete timer
        this.resetDeleteTimer();
    }

    // Start self-deletion timer
    startDeleteTimer() {
        this.timer = setTimeout(() => {
            console.log(`${this.callSign} not updated, removing from collection.`);
            this.destroy();
        }, this.deleteAfterSeconds);
    }

    // Reset deletion timer if update is received
    resetDeleteTimer() {
        if (this.timer) {
            clearTimeout(this.timer);
        }
        this.startDeleteTimer();
    }

    // Remove plane from map and collection
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