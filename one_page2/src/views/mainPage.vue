<template>
    <div>
        <b-button v-b-toggle.collapse-1 variant="primary">Toggle Collapse</b-button>
        <b-collapse id="collapse-1" class="mt-2">
            <b-card>
                <p class="card-text">Collapse contents Here</p>
                <b-button v-b-toggle.collapse-1-inner size="sm">Toggle Inner Collapse</b-button>
                <b-collapse id="collapse-1-inner" class="mt-2">
                    <b-card>Hello!</b-card>
                </b-collapse>
            </b-card>
        </b-collapse>

        <div id="map" style="width: 100%; height: 100vh;"></div>
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
