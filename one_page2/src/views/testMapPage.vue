<template>
    <div>
        <!-- Карта MapLibre -->
        <div id="map"></div>

        <!-- Кнопка для повторного запуска анимации -->
        <div class="overlay">
            <button @click="replay">Replay</button>
        </div>
    </div>
</template>

<script>
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import * as turf from 'turf';

export default {
    data() {
        return {
            map: null, // Экземпляр карты
            counter: 0, // Счётчик для анимации
            origin: [-122.414, 37.776], // Исходная точка (Сан-Франциско)
            destination: [-77.032, 38.913], // Конечная точка (Вашингтон)
            route: {}, // Данные маршрута
            point: {}, // Данные для точки
        };
    },
    mounted() {
        // Инициализация карты MapLibre
        this.initializeMap();
    },
    methods: {
        // Метод инициализации карты
        initializeMap() {
            this.map = new maplibregl.Map({
                container: 'map',
                style: 'https://api.maptiler.com/maps/streets/style.json?key=get_your_own_OpIi9ZULNHzrESv6T2vL',
                center: [-96, 37.8],
                zoom: 3
            });

            // Инициализация маршрута и точки
            this.setupRoute();

            this.map.on('load', this.startAnimation);
        },

        // Метод для подготовки маршрута
        setupRoute() {
            // Определение маршрута от исходной точки к конечной
            this.route = {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'LineString',
                            'coordinates': [this.origin, this.destination]
                        }
                    }
                ]
            };

            // Инициализация точки, которая будет анимироваться вдоль маршрута
            this.point = {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'properties': {},
                        'geometry': {
                            'type': 'Point',
                            'coordinates': this.origin
                        }
                    }
                ]
            };

            // Вычисляем расстояние маршрута и создаем "дугу" для анимации
            const lineDistance = turf.lineDistance(this.route.features[0], 'kilometers');
            const arc = [];
            const steps = 500; // Количество шагов для анимации

            for (let i = 0; i < lineDistance; i += lineDistance / steps) {
                const segment = turf.along(this.route.features[0], i, 'kilometers');
                arc.push(segment.geometry.coordinates);
            }

            this.route.features[0].geometry.coordinates = arc;
        },

        // Метод для начала анимации
        startAnimation() {
            // Добавление источников и слоев для маршрута и точки
            this.map.addSource('route', {
                'type': 'geojson',
                'data': this.route
            });

            this.map.addSource('point', {
                'type': 'geojson',
                'data': this.point
            });

            // Добавление слоя маршрута
            this.map.addLayer({
                'id': 'route',
                'source': 'route',
                'type': 'line',
                'paint': {
                    'line-width': 2,
                    'line-color': '#007cbf'
                }
            });

            // Добавление слоя для точки
            this.map.addLayer({
                'id': 'point',
                'source': 'point',
                'type': 'symbol',
                'layout': {
                    'icon-image': 'airport_15',
                    'icon-rotate': ['get', 'bearing'],
                    'icon-rotation-alignment': 'map',
                    'icon-overlap': 'always',
                    'icon-ignore-placement': true
                }
            });

            // Запуск анимации
            this.animatePoint();
        },

        // Метод анимации точки вдоль маршрута
        animatePoint() {
            // Обновляем координаты точки в зависимости от шага анимации
            this.point.features[0].geometry.coordinates = this.route.features[0].geometry.coordinates[this.counter];

            // Рассчитываем угол для поворота и ориентации точки по маршруту
            this.point.features[0].properties.bearing = turf.bearing(
                turf.point(this.route.features[0].geometry.coordinates[this.counter >= 1 ? this.counter - 1 : this.counter]),
                turf.point(this.route.features[0].geometry.coordinates[this.counter >= this.route.features[0].geometry.coordinates.length - 1 ? this.counter : this.counter + 1])
            );

            // Обновляем данные источника
            this.map.getSource('point').setData(this.point);

            // Если анимация не завершена, продолжаем
            if (this.counter < 500) {
                requestAnimationFrame(this.animatePoint);
            }

            // Увеличиваем счётчик
            this.counter++;
        },

        // Метод для повторного запуска анимации
        replay() {
            // Сброс координат точки в начальное положение
            this.point.features[0].geometry.coordinates = this.origin;

            // Обновление данных источника
            this.map.getSource('point').setData(this.point);

            // Сброс счётчика и повторный запуск анимации
            this.counter = 0;
            this.animatePoint();
        }
    }
};
</script>

<style scoped>
#map {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.overlay {
    position: absolute;
    top: 10px;
    left: 10px;
}

.overlay button {
    font: 600 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
    background-color: #3386c0;
    color: #fff;
    display: inline-block;
    margin: 0;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
    border-radius: 3px;
}

.overlay button:hover {
    background-color: #4ea0da;
}
</style>
