<template>
    <div>
        <div id="map" style="height: 100vh; width: 100%;"></div>
        <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow
            :visible="isSidebarVisible" :backdrop="false" @hidden="isSidebarVisible = false" bg-variant="light"
            text-variant="dark" left style="width: 180px; ">
            <template v-if="sidebarData">
                <b-card class="mb-2" header="header" header-bg-variant="primary" header-text-variant="white">
                    <b-table striped hover small :items="formattedSidebarData" :fields="tableFields"
                        responsive="sm"></b-table>
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
</style>