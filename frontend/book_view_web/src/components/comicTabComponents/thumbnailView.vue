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
              @click="clcikThumbnail(allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1].id)"></el-image>
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
                @confirm="clcikDeleteButton(allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1].id)"
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
    <el-row>
      <el-pagination background layout="prev, pager, next" :total="total" v-model:current-page="current_page"
                     @current-change="pageChange"/>
    </el-row>
  </div>
  <div v-if="this.fullScreenViewMode">
    <el-row>
      <el-button @click="clcikExitButton">退出全屏</el-button>
      <el-button @click="clickPreviousPic">上一页</el-button>
      <el-button @click="clickNextPic">下一页</el-button>
      <el-button>单/双页切换</el-button>
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
      <p>currentPage:{{ this.page }} -- bookLength:{{ this.CurrentBookLength }}</p>
    </el-row>
    <el-row>
      <el-image :src="viewPicUrl" @click="clickNextPic" fit="contain" usemap="#planetmap"></el-image>
    </el-row>
  </div>

</template>

<script>
import axios from "axios";
import {ElMessage} from 'element-plus'

export default {
  name: "thumbnailView",
  data() {
    return {
      allBooksDataSource: [],
      currentLibPage: 1,
      //当前缩略图视图的列数
      coverColNum: 2,
      //当前缩略图视图的行数
      row_conut: 1,
      //当前列表的页码
      current_page: 1,
      //当前book的总数
      total: 1,
      bookType: [
        '完结漫画', '连载漫画'
      ],
      fullScreenViewMode: false,
      drawer: false,
      //全屏模式下的bookid
      CurrentBookId: 1,
      //全屏模式下的页码数
      page: 1,
      //全屏模式下book的长度
      CurrentBookLength: 0,
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
      axios({
        method: 'get',
        url: `/comicManager/${id}/bookLength`,
        baseURL: 'http://172.17.18.115:8089'
      }).then(
          (response) => {
            console.log(response)
            if (response.status === 200) {
              console.log(response.data)
              this.CurrentBookLength = response.data
            }
          }
      ).catch(
          (err) => {
            console.log(err)
          }
      )
      console.log('fullScreenViewMode', this.fullScreenViewMode, this.CurrentBookId, this.CurrentBookLength)
    },
    clcikExitButton() {
      this.fullScreenViewMode = false
    },
    clcikImgLeft() {
      console.log('clcikImgLeft')
    },
    clcikImgRight() {
      console.log('clcikImgRight')
    },
    clcikDeleteButton(id) {
      console.log('clcikDeleteButton', id)
      axios({
        method: 'delete',
        url: `/comicManager/${id}/bookDelete`,
        baseURL: 'http://172.17.18.115:8089'
      }).then(
          (response) => {
            console.log(response)
            if (response.status === 204) {
              console.log(response.data)
              this.getAllBooks()
            }
          }
      ).catch(
          (err) => {
            console.log(err)
          }
      )
    },
    clickNextPic() {
      if (this.page + 1 > this.CurrentBookLength) {
        ElMessage({message: 'last page!', type: 'warning'})
      } else {
        this.page += 1
      }
    },
    clickPreviousPic() {
      if (this.page - 1 < 1) {
        ElMessage({message: 'first page!', type: 'warning'})
      } else {
        this.page -= 1
      }
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
              this.row_conut = Math.ceil(this.allBooksDataSource.length / this.coverColNum)
              console.log('getAllBooks', 'this.row_conut', this.row_conut, 'this.coverColNum', this.coverColNum, ' this.allBooksDataSource', this.allBooksDataSource)
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
