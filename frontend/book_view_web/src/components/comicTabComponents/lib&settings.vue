<template>
  <el-table :data="tableData" stripe style="width: 100%">
    <el-table-column prop="folderPath" label="folderPath" min-width="4"/>
    <el-table-column label="Operations" min-width="1">
      <template #default="scope">
        <!--        <el-button size="small" @click="handleEdit(scope.$index, scope.row)">Edit</el-button>-->
        <el-button
            size="small"
            type="danger"
            @click="handleDelete(scope.$index, scope.row)"
        >Delete
        </el-button
        >
      </template>
    </el-table-column>
  </el-table>
  <el-pagination background layout="prev, pager, next" :total="pathCount" :page-size="20"
                 v-model:current-page="currentLibPage"
                 @current-change="getLibPath"/>
  <el-input v-model="pathinput" placeholder="path">
    <template #prepend>path</template>
    <template #append>
      <el-button color="#3acf5f" @click="btnChange">submit</el-button>
    </template>
  </el-input>
  <el-button @click="startScan">scan comic libs</el-button>

</template>

<script>
import axios from "axios";

export default {
  name: "libSettings",
  data() {
    return {
      tableData: [],
      pathinput: '',
      pathCount: 0,
      currentLibPage: 1,
    }
  },
  mounted() {
    this.getLibPath()
  },
  methods: {
    getLibPath() {
      axios({
        method: 'get',
        url: '/comicManager/lib/',
        baseURL: 'http://172.17.18.115:8089',
        params: {'page': this.currentLibPage}
      }).then(
          (response) => {
            console.log(response)
            if (response.status === 200) {
              this.tableData = response.data.results
              this.pathCount = response.data.count
            }
          }
      ).catch(
          (err) => {
            console.log(err)
          }
      )
    },
    //  提交
    btnChange() {
      axios({
        method: 'post', url: '/comicManager/lib/', baseURL: 'http://172.17.18.115:8089', data: {
          'folderPath': this.pathinput
        }
      }).then(
          (response) => {
            if (response.status === 201) {
              console.log(response)
              this.getLibPath()
            }
          }
      ).catch(
          (err) => {
            console.log(err)
          }
      )
    },
    //删除
    handleDelete(e1, e2) {
      axios({method: 'delete', url: `/comicManager/lib/${e2.id}/`, baseURL: 'http://172.17.18.115:8089'}).then(
          (response) => {
            if (response.status === 204)
              console.log(response)
            this.getLibPath()
          }
      ).catch(
          (err) => {
            console.log(err)
          }
      )
    },
    //修改
    // handleEdit(e1, e2) {
    //   axios({method: 'put', url: `/comicManager/lib/${e2.id}/`, baseURL: 'http://172.17.18.115:8089'}).then(
    //       (response) => {
    //         if (response.status === 204)
    //           console.log(response)
    //         this.getLibPath()
    //       }
    //   ).catch(
    //       (err) => {
    //         console.log(err)
    //       }
    //   )
    // },
    startScan() {
      console.log('startScan')
      axios({
        method: 'get',
        url: '/comicManager/scan/',
        baseURL: 'http://172.17.18.115:8089'
      }).then(
          (response) => {
            console.log(response)
          }
      ).catch(
          (err) => {
            console.log(err)
          }
      )
    }
  }
}
</script>

<style scoped>

</style>
