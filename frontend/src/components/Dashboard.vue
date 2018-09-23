<template>
  <div>
    <h1>Dashboard</h1>
    <div class="main-dashboard">
      <div v-on:keydown="addNewTask($event)" class="add-new-task-container">
        <input id="new-task-title" type="text" placeholder="Task name" />
        <input id="new-task-description" type="text" placeholder="Task description" />
        <input type="button" value="Create Task" />
        <span id="new-task-error-message"></span>
      </div>
      <div v-for="task_data in orderedDashboardData" :key="task_data.id" :id="'task-' + task_data.id">
        <div class="specific-task">
          <h2 :id="'task-title-' + task_data.id" class="task-title" contenteditable=true v-on:blur="writeEditedDataToServer($event, 'task', task_data.id)" v-on:keydown="enterKey">
            {{ task_data.title }}
          </h2>
          <h3 :id="'task-description-' + task_data.id" class="task-description" contenteditable=true v-on:blur="writeEditedDataToServer($event, 'task', task_data.id)"
            v-on:keydown="enterKey">{{ task_data.description }}</h3>
        </div>
        <div class="task-buttons">
          <input type="button" @click="deleteTask(task_data.id); dashboardData.splice(dashboardData.indexOf(task_data.id), 1)" value="Delete" />
          <button class="reorder-todo" @click="reorderTodo">Reorder</button>
        </div>
        <ul>
          <li v-on:keydown="addNewTodo($event, task_data.id)" class="add-new-todo-container">
            <input :id="'new-todo-description-' + task_data.id" type="text" placeholder="Add Description" />
            <input :id="'new-todo-expiration-date-' + task_data.id" type="text" placeholder="YYYY-MM-DD HH:MM" />
            <input :id="'new-todo-tags-' + task_data.id" type="text" placeholder="insert comma separeted tags" />
            <span :id="'error-message-' + task_data.id"></span>
          </li>
          <li v-for="todo_data in orderedTodos(task_data.todos)" :key="todo_data.id" :id="'todo-' + todo_data.id">
            <div class="todo-list">
              <input type="checkbox" @click="toggleDoneFlag(task_data.id, todo_data.id)" v-model="todo_data.done_flag"/>
              <div class="checkbox-content">
                <h2 :id="'update-todo-description-' + todo_data.id" class="todo-description" contenteditable=true v-on:blur="writeEditedDataToServer($event, 'todo', task_data.id, todo_data.id)"
                  v-on:keydown="enterKey">
                  {{ todo_data.description }}
                </h2>
                <h3 :id="'update-todo-due-date-' + todo_data.id" class="todo-expdate" contenteditable=true v-on:blur="writeEditedDataToServer($event, 'todo', task_data.id, todo_data.id)"
                  v-on:keydown="enterKey">{{ todo_data.due_date }}</h3>
                <span :id="'todo-due-date-error-' + todo_data.id"></span>
                <input type="button" @click="deleteTodo(task_data.id, todo_data.id); task_data.todos.splice(task_data.todos.indexOf(todo_data), 1);" value="Delete"/>
              </div>
              <div class="tag-names-container">
                <span :id="'todo-' + todo_data.id + '-tag-change-' + tag_name" v-for="tag_name in todo_data.tags" :key="tag_name"
                  class="tag-name" contenteditable=true
                  v-on:blur="writeEditedDataToServer($event, 'tag', task_data.id, todo_data.id, tag_name)"
                v-on:keydown="enterKey">{{ tag_name }}</span>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
.main-dashboard {
  text-align: left;
  max-width: 800px;
  margin: 0 auto;

  .task-title {
    margin: 0;
  }

  .specific-task {
    display: inline-block;
  }
  .task-buttons {
    float: right;
  }

  .checkbox-content {
    display: inline-block;

    .todo-description {
      display: inline;
    }

    .todo-expdate {
      display: inline;
    }
  }

  .add-new-todo {
    display: block;
    clear: both;
  }
}

input[type=checkbox]:checked + div.checkbox-content{
  text-decoration: line-through;
}

.tag-name {
  margin: 0 5px;
}
</style>

<script>
import axios from 'axios'
import _ from 'lodash'

export default {
  data () {
    return {
      apiKey: '',
      dashboardData: [],
      orderedTodoList: [],
      reorderFlag: false,
      errorMessage: '',
      result1: null
    }
  },
  components: {
    'vue-datetime-picker': require('vue-datetime-picker')
  },
  computed: {
    orderedDashboardData: function () {
      return _.orderBy(this.dashboardData, 'updated_date', 'desc')
    }
  },
  created: function () {
    this.apiKey = localStorage.name
    generateTasks(this)
  },
  methods: {
    enterKey: function (event) {
      if (event.key === 'Enter') {
        document.activeElement.blur()
      }
    },
    writeEditedDataToServer: function (event, type, taskId, todoId, tagName) {
      if (type === 'task') {
        updateTask(this, taskId)
      } else if (type === 'todo') {
        updateTodo(this, taskId, todoId)
      } else if (type === 'tag') {
        updateTag(this, taskId, todoId, tagName)
      }
      console.log('New Name: ' + event.srcElement.outerText + ' of type: ' + type + ' taskid: ' + taskId + ' todoid: ' + todoId)
    },
    reorderTodo: function () {
      if (this.reorderFlag) {
        this.reorderFlag = false
      } else {
        this.reorderFlag = true
      }
    },
    orderedTodos: function (todoData) {
      if (this.reorderFlag) {
        todoData = _.orderBy(todoData, ['done_flag', 'due_date'])
      } else {
        todoData = _.orderBy(todoData, 'done_flag')
      }

      return todoData
    },
    addNewTask: function (event, taskId) {
      if (event.key === 'Enter') {
        var newTask = {
          'task': {
            'title': document.getElementById('new-task-title').value,
            'description': document.getElementById('new-task-description').value
          }
        }
        requestNewTask(this, newTask)
        generateTasks(this)
      }
    },
    deleteTask: function (taskId) {
      var token = localStorage.name
      var toggleAPI = this.$hostname + 'tasks/' + taskId + '/'
      axios.delete(toggleAPI, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error.response.data)
        })
    },
    toggleDoneFlag: function (taskId, todoId) {
      var token = localStorage.name
      var toggleAPI = this.$hostname + 'tasks/' + taskId + '/todos/' + todoId + '/toggle-done/'
      axios.patch(toggleAPI, null, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error.response.data)
        })
    },
    deleteTodo: function (taskId, todoId) {
      var token = localStorage.name
      var deleteTodoAPI = this.$hostname + 'tasks/' + taskId + '/todos/' + todoId + '/'
      axios.delete(deleteTodoAPI, {
        headers: {
          Authorization: 'Bearer ' + token
        }
      })
        .then(response => {
          console.log(response.data)
        })
        .catch(error => {
          console.log(error.response.data)
        })
    },
    addNewTodo: function (event, taskId) {
      if (event.key === 'Enter') {
        var newTodo = {
          'id': taskId,
          'todo': {
            'description': document.getElementById('new-todo-description-' + taskId).value,
            'due_date': document.getElementById('new-todo-expiration-date-' + taskId).value,
            'tags': document.getElementById('new-todo-tags-' + taskId).value || null
          }
        }
        requestNewTodo(this, newTodo)
        generateTasks(this)
      }
    }
  }
}

function requestNewTodo (vueInstance, newTodo) {
  var token = localStorage.name
  var tagList = null
  if (newTodo.todo.tags) {
    tagList = newTodo.todo.tags.split(',')
  }
  var trimmedTagList = tagList.map(tag => tag.trim())
  axios.post(vueInstance.$hostname + 'tasks/' + newTodo.id + '/todos/',
    {
      data: {
        description: newTodo.todo.description,
        due_date: newTodo.todo.due_date,
        tags: trimmedTagList
      }
    },
    {
      headers: {
        Authorization: 'Bearer ' + token
      }
    }
  )
    .then(response => {
      document.getElementById('error-message-' + newTodo.id).innerText = ''
      document.getElementById('new-todo-description-' + newTodo.id).value = ''
      document.getElementById('new-todo-expiration-date-' + newTodo.id).value = ''
      document.getElementById('new-todo-tags-' + newTodo.id).value = ''
    })
    .catch(error => {
      document.getElementById('error-message-' + newTodo.id).innerText = error.response.data.message.description
      this.errorMessage = error.response.data.message.description
    })
}

function requestNewTask (vueInstance, newTask) {
  var token = localStorage.name
  axios.post(vueInstance.$hostname + 'tasks/',
    {
      data: {
        title: newTask.task.title,
        due_date: newTask.task.description
      }
    },
    {
      headers: {
        Authorization: 'Bearer ' + token
      }
    }
  )
    .then(response => {
      document.getElementById('new-task-error-message').innerText = ''
      document.getElementById('new-task-title').value = ''
      document.getElementById('new-task-description').value = ''
    })
    .catch(error => {
      document.getElementById('new-task-title').innerText = error.response.data.message.description
      this.errorMessage = error.response.data.message.description
    })
}
function generateTasks (vueInstance) {
  var token = localStorage.name
  axios.get(vueInstance.$hostname + 'tasks/', {
    headers: {
      Authorization: 'Bearer ' + token
    }
  })
    .then(response => {
      var responseData = response.data.data
      console.log(responseData)
      vueInstance.dashboardData = responseData
    })
    .catch(error => {
      console.log('Error: ' + error.response)
      this.errorMessage = error.response.data.message.description
    })
}

function updateTask (vueInstance, taskId) {
  var token = localStorage.name
  axios.put(vueInstance.$hostname + 'tasks/' + taskId + '/', {
    data: {
      title: document.getElementById('task-title-' + taskId).innerText,
      description: document.getElementById('task-description-' + taskId).innerText
    }
  },
  {
    headers: {
      Authorization: 'Bearer ' + token
    }
  })
    .then(response => {
      console.log('Updated Task')
    })
    .catch(error => {
      console.log('Error: ' + error.response)
      this.errorMessage = error.response.data.message.description
    })
}

function updateTodo (vueInstance, taskId, todoId) {
  var token = localStorage.name
  console.log('update-todo-due-date-' + todoId)
  axios.put(vueInstance.$hostname + 'tasks/' + taskId + '/todos/' + todoId + '/', {
    data: {
      'description': document.getElementById('update-todo-description-' + todoId).innerText,
      'due_date': document.getElementById('update-todo-due-date-' + todoId).innerText
    }
  },
  {
    headers: {
      Authorization: 'Bearer ' + token
    }
  })
    .then(response => {
      document.getElementById('todo-due-date-error-' + todoId).innerText = ''
    })
    .catch(error => {
      document.getElementById('todo-due-date-error-' + todoId).innerText = error.response.data.message.description
      console.log('Error: ' + error.response)
      this.errorMessage = error.response.data.message.description
    })
}

function updateTag (vueInstance, taskId, todoId, tagName) {
  var token = localStorage.name
  var httpCall = vueInstance.$hostname + 'tasks/' + taskId +
    '/todos/' + todoId + '/tags/' + tagName + '/'
  var newTagName = document.getElementById('todo-' + todoId + '-tag-change-' + tagName).innerText
  axios.patch(httpCall, {
    data: {
      'new_name': newTagName
    }
  },
  {
    headers: {
      Authorization: 'Bearer ' + token
    }
  })
    .then(response => {
      var tagId = 'todo-' + todoId + '-tag-change-' + tagName
      document.getElementById(tagId).innerText = newTagName
      var newId = 'todo-' + todoId + '-tag-change-' + newTagName
      document.getElementById(tagId).id = newId
    })
    .catch(error => {
      document.getElementById('todo-due-date-error-' + todoId).innerText = error.response.data.message.description
      console.log('Error: ' + error.response)
      this.errorMessage = error.response.data.message.description
    })
}
</script>
