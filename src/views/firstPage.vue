<template>
  <b-row align-v="center" class="d-flex flex-wrap align-items-stretch">
    <test>
      <!-- 1 daļa-->
      <h1>{{ msg }}</h1>

      <input v-model="msg" />

      <button @click="reverseMessage">Reverse</button>
    </test>
    <test><!-- 2 daļa-->

      <p>
        <span :title="message"> <!-- span - show text when mouse over -->
          Hover your mouse over me for a few seconds to see my dynamically bound title!
        </span>
      </p>

      <p :style="{ color }" @click="changeColor">
        <!-- style with : to use variable color in {} | function name - changeColor  -->
        red, green or blue
      </p>
    </test>
    <test>
      <!-- 3 daļa-->
      <button style="margin: 0.25vw" @click="show = !show">
      <div v-if="show">show</div>
      <div v-else>hide</div>
    </button>
    <button style="margin: 0.25vw" @click="addName">add</button>
    <button style="margin: 0.25vw" @click="nameList.pop()">delete last</button>
    <button style="margin: 0.25vw" @click="nameList.reverse()">reverse list</button>

    <ul v-if="show && nameList.length">
      <li v-for="(exemplar,index) in nameList" :key="index">{{ exemplar }}</li>
    </ul>

    <p v-else-if="nameList.length">list is not empty, its hidden</p>
    <p v-else>list is empty</p>
    </test>
    <div class="w-100"></div>
    <test>
      <!-- 4 daļa-->
      <h1>Latest {{ repoName() }} commits at {{ currentBranch }} branch</h1>

<template v-for="branch in branches"><!-- create radio inputs for every branch -->
  <input type="radio" :id="branch" :value="branch" name="branch" v-model="currentBranch" :key="branch">
  <label :for="branch" :key="branch">{{ branch }}</label>
</template>

<p>{{ repoName() }}@{{ currentBranch }}</p>
<ul v-if="commits.length > 0">
  <li class="dala4" v-for="{ html_url, sha, author, commit } in commits" :key="sha" >
    <!-- create <li> for every example in commits array -->

    <a :href="html_url" target="_blank" class="commit">{{ sha.slice(0, 7) }}</a>
    <!-- display sha | slice(x,y) return simbols from x to y-1 -->

    - <span class="message">{{ truncate(commit.message) }}</span><br>
    <!-- display "-" than message | <br> - new line -->

    by <span class="author">
      <a :href="author.html_url" target="_blank">{{ commit.author.name }}</a> <!-- display author -->
    </span>

    at <span class="date" :title=timeHasPassed(commit.author.date)>{{ formatDate(commit.author.date) }}</span>
    <!-- display date and time -->
  </li>
</ul>
    </test>
    <test>
      <!-- 5 daļa-->
      <button id="id1 test" @click="greet">Greet</button>
    </test>
    <test>
      
    </test>
  </b-row>

</template>

<script setup>
import { ref } from 'vue';
import test from "@/components/slot.vue";


// Переменные и функции, которые будут использоваться в шаблоне
//  1 daļa
const msg = ref('Hello World!') //  ref() делает переменную реактивной (обновление ui где используется эта переменная) 

function reverseMessage() {
  msg.value = msg.value.split('').reverse().join('') //  text reverse
  setTimeout(() => notify('text is reversed'), 1) //  alert with timeout | function with parameter in setTimeout
}

function notify(text) {
  alert(text)
}
//  2 daļa
const message = ref("variable -> message")  //  ref() делает переменную реактивной (обновление ui где используется эта переменная) 
const color = ref('green')  //  ref() делает переменную реактивной (обновление ui где используется эта переменная) 

function changeColor() { // change variable color 
  if (color.value == 'green') {
    color.value = 'blue'
    return
  }

  if (color.value == 'blue') {
    color.value = 'red'
    return
  }

  if (color.value == 'red') {
    color.value = 'green'
    return
  }
}


//  3 daļa
const nameList = ref(['aleksandr', 'dmitrij', 'raimond'])
const show = ref(true)
const name = ref('')

function addName() {
  name.value = prompt("enter name:");//ugjkkjgkjhg
  nameList.value.push(name.value)
}



//  4 daļa
import { watchEffect } from 'vue'

const API_URL = `https://api.github.com/repos/nodejs/node/commits?per_page=4&sha=` //api link with objects
const branches = ['main', 'v6.x', 'fix-observe-large-arrays'] // which branche use (<<API_URL(...sha=)>> <<branche>>)

const currentBranch = ref(branches[0])
const commits = ref([]) //array to display commits

watchEffect(async () => {
    const url = `${API_URL}${currentBranch.value}`
    commits.value = await (await fetch(url)).json() // first await to wait for real answer | second await to wait extract data from the response
})

function truncate(v) {      //here take comit message example("doc: clarity to available addon options\n\nbullet pointed addon optons; wording clarity; fixes typo\n\nPR-URL: https://github.com/nodejs/node/pull/55715\nReviewed-By: Gireesh Punathil <gpunathi@in.ibm.com>\nReviewed-By: Antoine du Hamel <duhamelantoine1995@gmail.com>")
    //and take only "doc: clarity to available addon options" (until \n)
    const newline = v.indexOf('\n') // index of "\n" 
    return newline > 0 ? v.slice(0, newline) : v  // if-else condition ? if-true : if-false
}

function formatDate(v) {
    return v.replace(/T|Z/g, ' ') //original date "2024-11-06T07:55:49Z" to "2024-11-06 01:24:39"  |  /.../g find every "..." not only first
}

function repoName() {// take API_URL and return only name
    const start = API_URL.indexOf("repos/")
    const end = API_URL.indexOf("/commits")
    return API_URL.slice(start + 6, end)
}

function timeHasPassed(messageDate) { // return how much time has passed since messageDate in minutes
    let nowTime = new Date()
    let messageTime = new Date(messageDate)
    return  ((nowTime.getTime() - messageTime.getTime()) / 60000).toFixed(2) // toFixed(x) numbers after coma "x"
}

// 5 daļa
function greet(event) {
  alert(`Hello world!`)
  if (event) {
    alert(event.target.id + event.target.tagName) //display alert with element id and element tag name
  }
}
</script>