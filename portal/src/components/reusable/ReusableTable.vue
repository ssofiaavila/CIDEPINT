<template>
    <div class="table-responsive">
      <table>
        <thead>
          <tr>
            <th v-for="columna in columnNames" :key="columna">{{ columna }}</th>
            <th>{{buttonColumnName}}</th>
          </tr>
        </thead>
        <tbody v-for="item in items" :key="item.id">
          <tr>
            <td v-for="(value, key) in columnNames" :key="key">{{ item[key] }}</td>
            <td>
              <router-link :to="`${linkPrefix}/${item.id}`" class="btn btn-sm btn-primary">{{buttonText}}</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      columnNames: Object,
      items: Array,
      linkPrefix: String,
      buttonColumnName: String,
      buttonText: String,
    },
  };
  </script>