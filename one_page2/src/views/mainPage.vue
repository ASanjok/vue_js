<template>
    <div style="position: relative; height:90vh;">
        <!-- Collapse menu -->
        <b-button v-b-toggle.collapse-1 variant="primary" class="rounded-0" style="position: absolute;z-index: 10; top:-3vh; width: 33vw;">Toggle Collapse</b-button>
        <b-collapse id="collapse-1" class="mt-2" style="position: absolute; top:1vh; z-index: 10; width: 33vw;">
            <b-card style="position:absolute; z-index: 10;">
                <p class="card-text">Collapse contents Here</p>
                <b-button v-b-toggle.collapse-1-inner size="sm">Toggle Inner Collapse</b-button>
                <b-collapse id="collapse-1-inner" class="mt-2">
                    <b-card>Hello!</b-card>
                </b-collapse>
            </b-card>
        </b-collapse>

        <b-button v-b-toggle.collapse-2 variant="primary" class="rounded-0" style="position: absolute; left: 33vw; top:-3vh; width: 33vw; z-index: 10;">Toggle Collapse</b-button>
        <b-collapse id="collapse-2" class="mt-2" style="position: absolute; left: 33vw; top:1vh; width: 33vw; z-index: 10;">
            <b-card style="position:absolute; z-index: 10;">
                <p class="card-text">Collapse contents Here</p>
                <b-button v-b-toggle.collapse-1-inner size="sm">Toggle Inner Collapse</b-button>
                <b-collapse id="collapse-1-inner" class="mt-2">
                    <b-card>Hello!</b-card>
                </b-collapse>
            </b-card>
        </b-collapse>

        <b-button v-b-toggle.collapse-3 variant="primary" class="rounded-0" style="position: absolute; left: 66vw; top:-3vh; width: 34vw; z-index: 10;">Toggle Collapse</b-button>
        <b-collapse id="collapse-3" class="mt-2" style="position: absolute; left: 66vw; top:1vh; width: 34vw; z-index: 10;">
            <b-card style="position:absolute; z-index: 10;">
                <p class="card-text">Collapse contents Here</p>
                <b-button v-b-toggle.collapse-1-inner size="sm">Toggle Inner Collapse</b-button>
                <b-collapse id="collapse-1-inner" class="mt-2">
                    <b-card>Hello!</b-card>
                </b-collapse>
            </b-card>
        </b-collapse>

        <!-- Map container -->
        <div id="map" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></div>
    </div>
</template>

<script>
/* eslint-disable */
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

export default {
    name: 'MainPage',
    mounted() {
        this.initMap();
    },
    methods: {
        initMap() {
            const map = new maplibregl.Map({
                container: 'map', // container id
                style: 'https://api.maptiler.com/maps/outdoor-v2/style.json?key=SNBPG5wFM6FhUXbN07ua', // style URL
                center: [24.562966769607783, 56.798003718105406], // starting position [lng, lat]
                zoom: 6.743059121016559, // starting zoom
                minZoom: 5.5,
                maxZoom: 9,
            });

            // Получение текущих координат центра карты
            const currentCenter = map.getCenter();
            const currentZoom = map.getZoom();
            console.log('current zoom:', currentZoom); // Выведет текущие координаты в консоль

            // Отслеживание изменения центра карты
            map.on('moveend', () => {
                const newCenter = map.getCenter();
                const zoomvalue = map.getZoom();
                console.log('New center after move:', newCenter);
                console.log('New zoom after move - ', zoomvalue);
            });
        }
    }
}
</script>

<style scoped>
#map {
    position: absolute; /* Ensure the map covers the whole screen */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
</style>
