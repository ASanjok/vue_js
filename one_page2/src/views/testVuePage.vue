<template>
  <b-row align-v="center" class="d-flex flex-wrap align-items-stretch justify-content-start">
    <slotFromComponent>
      <!-- Part 1 -->
      <div class="container py-4"> <!-- Container with padding (Bootstrap) -->
        <h1 class="text-center mb-4">{{ msg }}</h1> <!-- Centered title with bottom margin -->

        <div class="mb-3"> <!-- Margin for input -->
          <label for="msgInput" class="form-label">Enter a message:</label> <!-- Label for input -->
          <input id="msgInput" type="text" v-model="msg" class="form-control" />
          <!-- Using Bootstrap classes for input field -->
        </div>

        <button @click="reverseMessage" class="btn btn-primary"> <!-- Button with Bootstrap styling -->
          Reverse
        </button>
      </div>
    </slotFromComponent>
    <slotFromComponent><!-- Part 2 -->
      <div class="card p-3 border-secondary">
        <!-- Card with content -->
        <p>
          <span :title="message" class="text-info">
            <!-- span - show text when mouse over -->
            Hover your mouse over me for a few seconds to see my dynamically bound title!
          </span>
        </p>

        <p :style="{ color }" @click="changeColor" class="cursor-pointer">
          <!-- Text that changes color on click -->
          <span class="font-weight-bold">
            Red, Green, or Blue
          </span>
        </p>
      </div>

    </slotFromComponent>
    <slotFromComponent>
      <!-- Part 3 -->
      <b-button variant="success" style="margin: 0.25vw" @click="show = !show">
        <div v-if="show">show</div>
        <div v-else>hide</div>
      </b-button>
      <button style="margin: 0.25vw" @click="addName" class="btn btn-primary">add</button>
      <button style="margin: 0.25vw" @click="nameList.pop()" class="btn">delete last</button>
      <button style="margin: 0.25vw" @click="nameList.reverse()" class="btn btn-danger">reverse list</button>

      <b-list-group v-if="show && nameList.length">
        <b-list-group-item v-for="(exemplar, index) in nameList" :key="index">{{ exemplar }}</b-list-group-item>
      </b-list-group>

      <p v-else-if="nameList.length">list is not empty, its hidden</p>
      <p v-else>list is empty</p>
    </slotFromComponent>
    <div class="w-100"></div>
    <slotFromComponent>
      <!-- Part 4 -->
      <h1>Latest {{ repoName() }} commits at {{ currentBranch }} branch</h1>

      <template v-for="branch in branches"><!-- Create radio inputs for every branch -->
        <b-form-radio :id="branch" :value="branch" v-model="currentBranch" :key="branch" class="d-flex align-items-center"> {{ branch }} </b-form-radio>
      </template>

      <p>{{ repoName() }}@{{ currentBranch }}</p>
      <b-list-group v-if="commits.length > 0">
        <b-list-group-item class="dala4" v-for="{ html_url, sha, author, commit } in commits" :key="sha">
          <!-- Create <li> for every example in commits array -->

          <a :href="html_url" target="_blank" class="commit">{{ sha.slice(0, 7) }}</a>
          <!-- Display sha | slice(x,y) returns symbols from x to y-1 -->

          - <span class="message">{{ truncate(commit.message) }}</span><br>
          <!-- Display "-" then message | <br> - new line -->

          by <span class="author">
            <a :href="author.html_url" target="_blank">{{ commit.author.name }}</a> <!-- Display author -->
          </span>

          at <span class="date" :title=timeHasPassed(commit.author.date)>{{ formatDate(commit.author.date) }}</span>
          <!-- Display date and time -->
        </b-list-group-item>
      </b-list-group>
    </slotFromComponent>
    <slotFromComponent>
      <!-- Part 5 -->
      <b-button id="id1 test" @click="greet" class="mx-auto">Greet</b-button>
    </slotFromComponent>
    <slotFromComponent>

    </slotFromComponent>
  </b-row>

</template>

<script setup>
import { ref } from 'vue';
import slotFromComponent from "@/components/slot.vue";


// Variables and functions that will be used in the template
// Part 1
const msg = ref('Hello World!') // ref() makes the variable reactive (UI updates wherever this variable is used)

function reverseMessage() {
  msg.value = msg.value.split('').reverse().join('') // Reverse the text
  setTimeout(() => notify('text is reversed'), 1) // Alert with timeout | Function with parameter in setTimeout
}

function notify(text) {
  alert(text)
}
// Part 2
const message = ref("variable -> message")  // ref() makes the variable reactive (UI updates wherever this variable is used)
const color = ref('green')  // ref() makes the variable reactive (UI updates wherever this variable is used)

function changeColor() { // Change variable color
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


// Part 3
const nameList = ref(['aleksandr', 'dmitrij', 'raimond'])
const show = ref(true)
const name = ref('')

function addName() {
  name.value = prompt("enter name:");// Prompt for name input
  nameList.value.push(name.value) // Add name to the list
}


// Part 4
import { watchEffect } from 'vue'

const API_URL = `https://api.github.com/repos/nodejs/node/commits?per_page=4&sha=` // API link with objects
const branches = ['main', 'v6.x', 'fix-observe-large-arrays'] // Which branch to use (<<API_URL(...sha=)>> <<branch>>)

const currentBranch = ref(branches[0])
const commits = ref([]) // Array to display commits

watchEffect(async () => {
  const url = `${API_URL}${currentBranch.value}`
  commits.value = await (await fetch(url)).json() // First await to wait for the real answer | Second await to extract data from the response
})

function truncate(v) {      // Here take commit message example("doc: clarity to available addon options\n\nbullet pointed addon options; wording clarity; fixes typo\n\nPR-URL: https://github.com/nodejs/node/pull/55715\nReviewed-By: Gireesh Punathil <gpunathi@in.ibm.com>\nReviewed-By: Antoine du Hamel <duhamelantoine1995@gmail.com>") 
  // and take only "doc: clarity to available addon options" (until \n)
  const newline = v.indexOf('\n') // Index of "\n"
  return newline > 0 ? v.slice(0, newline) : v  // if-else condition ? if-true : if-false
}

function formatDate(v) {
  return v.replace(/T|Z/g, ' ') // Original date "2024-11-06T07:55:49Z" to "2024-11-06 01:24:39" | /.../g find every "..." not only the first
}

function repoName() {// Take API_URL and return only the name
  const start = API_URL.indexOf("repos/")
  const end = API_URL.indexOf("/commits")
  return API_URL.slice(start + 6, end)
}

function timeHasPassed(messageDate) { // Return how much time has passed since messageDate in minutes
  let nowTime = new Date()
  let messageTime = new Date(messageDate)
  return ((nowTime.getTime() - messageTime.getTime()) / 60000).toFixed(2) // toFixed(x) numbers after comma "x"
}

// Part 5
function greet(event) {
  alert(`Hello world!`)
  if (event) {
    alert(event.target.id + event.target.tagName) // Display alert with element id and element tag name
  }
}
</script>
