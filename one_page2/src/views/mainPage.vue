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

                    <b-nav-item-dropdown text="Lang" right>
                        <b-dropdown-item href="#">EN</b-dropdown-item>
                        <b-dropdown-item href="#">ES</b-dropdown-item>
                        <b-dropdown-item href="#">RU</b-dropdown-item>
                        <b-dropdown-item href="#">FA</b-dropdown-item>
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
    </div>
</template>

<script>
/* eslint-disable */
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

export default {
    mounted() {
        // Инициализация карты в хуке mounted
        const map = new maplibregl.Map({
            container: 'map',
            style: 'https://api.maptiler.com/maps/outdoor-v2/style.json?key=SNBPG5wFM6FhUXbN07ua',
            center: [29, 40], // начальная позиция [lng, lat]
            zoom: 2,
            minZoom: 5.5,
            maxZoom: 9,
        });

        map.on('moveend', () => {
            const newCenter = map.getCenter(); // выводим в консоль для проверки
            const zoomValue = map.getZoom();
            console.log('New center after move:', newCenter);
            console.log('New zoom after move - ', zoomValue);
        });

        map.on('load', () => {
            // Когда карта загружена, выполняем полёт
            map.flyTo({
                center: [24.56, 56.79],
                zoom: 6,
                bearing: 0,
                speed: 0.5,
                curve: 0.1,
                easing(t) {
                    if (t < 2) {
                        t = t * (2 - t)
                    }
                    return t;
                },
                essential: true,
            });
        });


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
