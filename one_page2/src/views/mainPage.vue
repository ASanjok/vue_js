<template>
    <div id="map" style="width: 100%; height: 100vh;"></div>
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
                style: 'https://demotiles.maplibre.org/style.json', // style URL
                center: [24.562966769607783, 56.798003718105406], // starting position [lng, lat]
                zoom: 6.743059121016559 // starting zoom
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
