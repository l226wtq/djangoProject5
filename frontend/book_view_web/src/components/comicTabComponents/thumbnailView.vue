<template>
  <div v-show="!this.fullScreenViewMode">
    <el-row>
      <el-input-number v-model="coverColNum" @change="colChange" :min="1" :max="10"/>
      <el-pagination background layout="prev, pager, next" :total="total" v-model:current-page="current_page"
                     @current-change="pageChange"/>
    </el-row>

    <el-row v-for="row_num in row_conut" :key="row_num" ref="el_row">
      <el-col v-for="col_num in coverColNum" :key='col_num' :span="Math.floor(24/coverColNum)">
        <!--      单个缩略图框-->
        <div v-if="(row_num - 1) * coverColNum + col_num - 1<this.allBooksDataSource.length">
          <p>{{ allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1].title }}</p>
          <el-image
              :src="`http://172.17.18.115:8089/static/covers/${allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1]?.id}.webp`"
              @click="clcikThumbnail(allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1]?.id)"></el-image>
          <el-row>
            <el-col :span="12">
              <el-input
                  clearable
                  noShadow
                  v-model="allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1].author"
              />
            </el-col>
            <el-col :span="12">
              <el-date-picker
                  class="cover-date-picker"
                  type="date"
                  placeholder="选择日期"
                  size="default"
                  value-format="YYYY-MM-DD"
              />
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12"
            >
              <el-rate v-model="allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1].rating"
              />
            </el-col>
            <el-col :span="12">
              <el-select
                  class="m-2"
                  placeholder="选择类型"
              >
                <el-option
                    v-for="tp in bookType"
                    :key="tp"
                    :label="tp"
                    :value="tp"
                />
              </el-select>
            </el-col>
          </el-row>
          <el-row class="mb-2">
            <el-button
                type="warning"
            >编辑
            </el-button
            >
            <el-button
                type="warning"
            >保存
            </el-button
            >
            <el-popconfirm
                title="确定要删除吗?"
                confirm-button-text="确认"
                cancel-button-text="手滑了"
            >
              <template #reference>
                <el-button type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </el-row>
        </div>

        <!--      <el-image-->
        <!--          :src="`http://172.17.18.115:8089/static/covers/${allBooksDataSource[(row_num-1)*coverColNum+col_num-1]?.id}.webp`"></el-image>-->
      </el-col>
    </el-row>
  </div>
  <div v-show="this.fullScreenViewMode">
    <el-row>
      <el-button @click="clcikExitButton">退出全屏</el-button>
      <el-button type="primary" style="margin-left: 16px" @click="drawer = true">
        打开抽屉
      </el-button>
      <el-drawer
          v-model="drawer"
          title="I am the title"
          direction="btt"
      >
        <span>Hi, there!</span>
      </el-drawer>
    </el-row>
    <el-row>
      <el-image :src="viewPicUrl" @click="clickNextPic" fit="contain"></el-image>
    </el-row>
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "thumbnailView",
  data() {
    return {
      allBooksDataSource: [],
      currentLibPage: 1,
      coverColNum: 2,
      row_conut: 1,
      current_page: 1,
      total: 1,
      bookType: [
        '完结漫画', '连载漫画'
      ],
      fullScreenViewMode: false,
      drawer: false,
      CurrentBookId: 1,
      page: 1,
    }
  },
  computed: {
    viewPicUrl() {
      return `http://172.17.18.115:8089/comicManager/${this.CurrentBookId}/bookPic/?page=${this.page}`;
    }
  },
  created() {
    console.log('执行了create')
    // this.getAllBooks()

  },
  mounted() {
    this.getAllBooks()
  },

  methods: {
    colChange(col_num) {
      console.log(this.allBooksDataSource)
      const count = this.allBooksDataSource.length
      this.row_conut = Math.ceil(count / col_num)
    },
    pageChange(e) {
      console.log(e, this.current_page)
      this.getAllBooks()
    },
    clcikThumbnail(id) {
      this.fullScreenViewMode = true
      this.CurrentBookId = id
      this.page = 1
      console.log('fullScreenViewMode', this.fullScreenViewMode, this.CurrentBookId)
    },
    clcikExitButton() {
      this.fullScreenViewMode = false
    },
    clickNextPic() {
      this.page += 1
    },
    getAllBooks() {
      axios({
        method: 'get',
        url: '/comicManager/',
        baseURL: 'http://172.17.18.115:8089',
        params: {'page': this.current_page}
      }).then(
          (response) => {
            console.log(response)
            if (response.status === 200) {
              this.allBooksDataSource = response.data.results
              this.total = response.data.count
              this.row_conut = Math.floor(this.allBooksDataSource.length / this.coverColNum)
              console.log('this.row_conut, this.coverColNum', this.row_conut, this.coverColNum, this.allBooksDataSource, response.data)
              // this.pathCount = response.data.count
            }
          }
      ).catch(
          (err) => {
            console.log(err)
          }
      )
    },
  }
}
</script>

<style scoped>

</style>
