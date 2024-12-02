<template>
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">NavBar</b-navbar-brand>

            <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

            <b-collapse id="nav-collapse" is-nav>
                <b-navbar-nav>
                    <b-nav-item href="#">Link</b-nav-item>
                    <b-nav-item href="#" disabled>Disabled</b-nav-item>
                </b-navbar-nav>

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <b-nav-form>
                        <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
                        <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
                    </b-nav-form>

                    <b-nav-item-dropdown :text="currentStyle.name" right>
                        <b-dropdown-item v-for="style in styles" :key="style.name" @click="changeMapStyle(style)">
                            {{ style.name }}
                        </b-dropdown-item>
                    </b-nav-item-dropdown>

                    <b-nav-item-dropdown right>
                        <!-- Using 'button-content' slot -->
                        <template #button-content>
                            <em>User</em>
                        </template>
                        <b-dropdown-item href="#">Profile</b-dropdown-item>
                        <b-dropdown-item href="#">Sign Out</b-dropdown-item>
                    </b-nav-item-dropdown>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
        <!-- Map container Maplibre gl js-->
        <div id="map"></div>
        <div v-if="coordinates"
            class="position-absolute bottom-0 start-0 p-2 bg-dark bg-opacity-50 text-white fs-6 lh-sm">
            Longitude: {{ coordinates.lng }}<br />
            Latitude: {{ coordinates.lat }}<br />
            Zoom: {{ zoom }}
        </div>

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
            map: null,
            startCoordinates: [24.7, 56.9],
            coordinates: null,
            zoom: null,

            route: null,
            point: null,
            counter: 0,

            poligon: null,

            styles: [
                { name: 'liberty', url: 'https://tiles.openfreemap.org/styles/liberty' },
                { name: 'bright', url: 'https://tiles.openfreemap.org/styles/bright' },
                { name: 'dark', url: 'https://tiles.openfreemap.org/styles/dark' },
            ],
            currentStyle: { name: 'liberty', url: 'https://tiles.openfreemap.org/styles/liberty' },
        };
    },
    mounted() {
        this.map = new maplibregl.Map({
            container: 'map',
            style: 'https://tiles.openfreemap.org/styles/liberty',
            center: this.startCoordinates,
            zoom: 6.5,
        });

        this.map.on('moveend', () => {
            this.coordinates = this.map.getCenter();
            this.zoom = this.map.getZoom();
        });

        this.map.on('load', () => {
            this.startAnimation();
            this.createPoligon();
        });
    },
    methods: {
        changeMapStyle(style) {
            this.map.setStyle(style.url);
            this.currentStyle = style;

            // Используем событие 'styledata', чтобы дождаться окончания загрузки стиля
            this.map.on('styledata', () => {
                // После изменения стиля, создаем слои и источники заново, если их нет
                if (!this.map.getSource('route')) {
                    this.map.addSource('route', {
                        'type': 'geojson',
                        'data': this.route
                    });
                }

                if (!this.map.getSource('point')) {
                    this.map.addSource('point', {
                        'type': 'geojson',
                        'data': this.point
                    });
                }

                if (!this.map.getLayer('route')) {
                    this.map.addLayer({
                        'id': 'route',
                        'source': 'route',
                        'type': 'line',
                        'paint': {
                            'line-width': 2,
                            'line-color': '#007cbf'
                        }
                    });
                }

                if (!this.map.getLayer('point')) {
                    this.map.addLayer({
                        'id': 'point',
                        'source': 'point',
                        'type': 'circle',
                        'paint': {
                            'circle-radius': 10,
                            'circle-color': '#ff0000'
                        }
                    });
                }

                // Перезапускаем анимацию
                this.animatePoint();
            });
        },

        createPoligon() {
            this.map.addSource('source', {
                'type': 'geojson',
                'data': {
                    'type': 'Feature',
                    'properties': {},
                    'geometry': {
                        'type': 'Polygon',
                        'coordinates': [
                            [
                                [24.19637, 56.94769],
                                [24.21724, 56.94479],
                                [24.21453, 56.93785],
                                [24.21893, 56.93706],
                                [24.22158, 56.93572],
                                [24.21123, 56.93165],
                                [24.19576, 56.93220],
                                [24.19637, 56.94769],
                            ]
                        ]
                    }
                }
            });
            this.map.addLayer({
                'id': 'pattern-layer',
                'type': 'fill',
                'source': 'source',
                'paint': {
                    'fill-color': '#ff0000',
                    'fill-opacity': 0.5
                }
            });
        },

        createRout() { // create full route
            this.route = {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': [[25.2, 58.1], [26.6, 55.7], [20.9, 56.4], [28.2, 56.3]]
                        }
                    }
                ]
            };
        },

        createPoint() { // create a point that is going to be animated
            this.point = {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'properties': {},
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [25.2, 58.1]
                        }
                    }
                ]
            };

            const lineDistance = turf.lineDistance(this.route.features[0], 'kilometers'); // find distance of route in kilomenters
            const routeArc = [];
            const steps = 300; // how many steps will be in animation

            for (let i = 0; i < lineDistance; i += lineDistance / steps) {
                const segment = turf.along(this.route.features[0], i, 'kilometers');
                routeArc.push(segment.geometry.coordinates);
            }

            this.route.features[0].geometry.coordinates = routeArc;
        },

        startAnimation() {
            this.createRout()
            this.createPoint()

            if (!this.map.getSource('route')) { // create a layer with route and point
                this.map.addSource('route', {
                    'type': 'geojson',
                    'data': this.route
                });
            }

            if (!this.map.getSource('point')) {
                this.map.addSource('point', {
                    'type': 'geojson',
                    'data': this.point
                });
            }

            if (!this.map.getLayer('route')) { // add style property for route and point
                this.map.addLayer({
                    'id': 'route',
                    'source': 'route',
                    'type': 'line',
                    'paint': {
                        'line-width': 2,
                        'line-color': '#007cbf'
                    }
                });
            }

            if (!this.map.getLayer('point')) {
                this.map.addLayer({
                    'id': 'point',
                    'source': 'point',
                    'type': 'circle',
                    'paint': {
                        'circle-radius': 10,
                        'circle-color': '#ff0000'
                    }
                });
            }

            this.animatePoint();
        },

        animatePoint() {

            // check for point, to not be outside of coordinate array
            if (this.counter >= this.route.features[0].geometry.coordinates.length) {
                console.error("Counter exceeded available route coordinates.");
                return;
            }

            const currentCoord = this.route.features[0].geometry.coordinates[this.counter];
            const prevCoord = this.route.features[0].geometry.coordinates[this.counter >= 1 ? this.counter - 1 : this.counter];
            const nextCoord = this.route.features[0].geometry.coordinates[this.counter >= this.route.features[0].geometry.coordinates.length - 1 ? this.counter : this.counter + 1];

            // check for coordinates
            if (!Array.isArray(currentCoord) || !Array.isArray(prevCoord) || !Array.isArray(nextCoord)) {
                console.error("Invalid coordinates:", { currentCoord, prevCoord, nextCoord });
                return;
            }

            // update point coordinate
            this.point.features[0].geometry.coordinates = currentCoord;

            // calculate angle for point
            this.point.features[0].properties.bearing = turf.bearing(turf.point(prevCoord), turf.point(nextCoord));

            // update point coordinate on map
            this.map.getSource('point').setData(this.point);

            if (this.counter < this.route.features[0].geometry.coordinates.length - 1) {
                setTimeout(() => {
                    this.counter++;
                    this.animatePoint();
                }, 20);
            }
        },


    }
};
</script>

<style scoped>
#map {
    position: absolute;
    /* Ensure the map covers the whole screen */
    top: 112px;
    left: 0;
    width: 100%;
    height: calc(100% - 112px);
}
</style>
