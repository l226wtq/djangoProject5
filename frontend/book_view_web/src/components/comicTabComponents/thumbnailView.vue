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
              :src="`${api}/static/covers/${allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1]?.id}.webp`"
              @click="clcikThumbnail(allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1].id)"></el-image>
          <el-row>

            <el-col :span="12">
              <el-input
                  clearable
                  noShadow
                  :disabled="!editMode[(row_num - 1) * coverColNum + col_num - 1]"
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
                  :disabled="!editMode[(row_num - 1) * coverColNum + col_num - 1]"
              />
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12"
            >
              <el-rate v-model="allBooksDataSource[(row_num - 1) * coverColNum + col_num - 1].rating"
                       :disabled="!editMode[(row_num - 1) * coverColNum + col_num - 1]"
              />
            </el-col>
            <el-col :span="12">
              <el-select
                  class="m-2"
                  placeholder="选择类型"
                  :disabled="!editMode[(row_num - 1) * coverColNum + col_num - 1]"
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
                :type="this.editMode[(row_num - 1) * coverColNum + col_num - 1] ? 'info' : 'primary'"
                @click="this.editMode[(row_num - 1) * coverColNum + col_num - 1]=!this.editMode[(row_num - 1) * coverColNum + col_num - 1]"
                ref="editButton"
            >{{
                editMode[(row_num - 1) * coverColNum + col_num - 1] ? editCancelButtonText : editButtonText
              }}
            </el-button
            >
            <el-button
                @click="clickSaveButton(allBooksDataSource[(row_num-1)* coverColNum+col_num-1],(row_num-1)* coverColNum+col_num-1)"
                :disabled="!this.editMode[(row_num - 1) * coverColNum + col_num - 1]"
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

        <!--        <el-image-->
        <!--            :src="`${process.env.VUE_APP_BASE_URL}/static/covers/${allBooksDataSource[(row_num-1)*coverColNum+col_num-1]?.id}.webp`"></el-image>-->
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
      <el-button v-if="dualPageEnable" @click="clickPageMatch">页码匹配</el-button>
      <el-button type="primary" style="margin-left: 16px" @click="drawer = true">
        更多设置
      </el-button>

      <el-drawer
          v-model="drawer"
          title="更多设置"
          direction="btt"
      >
        <el-row class="moresetting">
          <el-switch
              v-model="this.dualPageEnable"
              style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
              active-text="双页显示"
              inactive-text="单页显示"
          />
          <el-switch
              v-model="this.ImgHeightMode"
              style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
              active-text="浏览器一页模式"
              inactive-text="图片高度模式"
          />
        </el-row>
        <br/>
        <el-switch
            v-model="this.showCoverSeparately"
            style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
            active-text="单独显示封面"
            inactive-text="合并显示封面"
        />

        <!--        <el-button @click="clickDualPageEnable">单/双页切换</el-button>-->
      </el-drawer>
      <el-slider class="page_slider" v-model="this.page" :min="1" :max="this.CurrentBookLength">page</el-slider>
      <!--      <p>currentPage:{{ this.page }} &#45;&#45; bookLength:{{ this.CurrentBookLength }}</p>-->

    </el-row>
    <el-row class="fullScreenContainer">
      <img v-if="dualPageEnableComputed" :src="viewPicUrlPlusOne" @click="clickNextPic" class="fullScreenImg">
      <img :src="viewPicUrl" @click="clickNextPic" class="fullScreenImg">
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
      editMode: [],
      drawer: false,
      //全屏模式下的bookid
      CurrentBookId: 1,
      //全屏模式下的页码数
      page: 1,
      //全屏模式下book的长度
      CurrentBookLength: 1,
      editButtonText: '编辑',
      editCancelButtonText: '取消编辑',
      dualPageEnable: false,
      showCoverSeparately: true,
      ImgHeightMode: true,
      api: '',
    }
  },
  computed: {
    viewPicUrl() {
      return `${process.env.VUE_APP_BASE_URL}/comicManager/${this.CurrentBookId}/bookPic/?page=${this.page}`;
    },
    viewPicUrlPlusOne() {
      return `${process.env.VUE_APP_BASE_URL}/comicManager/${this.CurrentBookId}/bookPic/?page=${this.page + 1}`;
    },
    dualPageEnableComputed() {
      if (this.showCoverSeparately) {
        if (this.dualPageEnable) {
          if (this.page === 1) {
            return false
          } else {
            return this.page + 1 <= this.CurrentBookLength;
          }
        } else {
          return false
        }
      } else {
        if (this.dualPageEnable) {
          if (this.page === 1) {
            return true
          } else {
            return this.page + 1 <= this.CurrentBookLength;
          }
        } else {
          return false
        }
      }
    }
  },
  created() {
    console.log('执行了create')
    // this.getAllBooks()
    this.api = process.env.VUE_APP_BASE_URL
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
        baseURL: process.env.VUE_APP_BASE_URL
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
    clickSaveButton(data, index) {
      console.log('clickSaveButton', data, index)
      this.editOneBook(data, index)

    },
    clickDualPageEnable() {
      this.dualPageEnable = !this.dualPageEnable
    },
    clickPageMatch() {
      if (this.page + 1 > this.CurrentBookLength) {
        ElMessage({message: 'last page!', type: 'warning'})
      } else {
        this.page += 1
      }
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
        baseURL: process.env.VUE_APP_BASE_URL
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
      if (this.dualPageEnableComputed) {
        if (this.page + 2 > this.CurrentBookLength) {
          ElMessage({message: 'last page!', type: 'warning'})
        } else {
          this.page += 2
        }
      } else {
        if (this.page + 1 > this.CurrentBookLength) {
          ElMessage({message: 'last page!', type: 'warning'})
        } else {
          this.page += 1
        }
      }

    },
    clickPreviousPic() {
      if (this.dualPageEnable && this.page !== 2) {
        if (this.page - 2 < 1) {
          ElMessage({message: 'first page!11111111111', type: 'warning'})
        } else {
          this.page -= 2
        }
      } else {
        if (this.page - 1 < 1) {
          ElMessage({message: 'first page!22222222222', type: 'warning'})
        } else {
          this.page -= 1
        }
      }

    },
    getAllBooks() {
      axios({
        method: 'get',
        url: '/comicManager/',
        baseURL: process.env.VUE_APP_BASE_URL,
        params: {'page': this.current_page}
      }).then(
          (response) => {
            console.log(response)
            if (response.status === 200) {
              this.allBooksDataSource = response.data.results
              this.total = response.data.count
              this.row_conut = Math.ceil(this.allBooksDataSource.length / this.coverColNum)
              this.editMode = new Array(this.row_conut * this.coverColNum).fill(false)
              console.log('getAllBooks', 'this.row_conut', this.row_conut, 'this.coverColNum', this.coverColNum, ' this.allBooksDataSource', this.allBooksDataSource, 'editMode', this.editMode)
              // this.pathCount = response.data.count

            }
          }
      ).catch(
          (err) => {
            console.log(err)
          }
      )
    },
    editOneBook(bookData, index) {
      axios({
        method: 'put',
        url: `/comicManager/${bookData.id}/`,
        baseURL: process.env.VUE_APP_BASE_URL,
        data: {
          "author": bookData.author,
          "publishDate": bookData.publishDate,
          "rating": bookData.rating,
          "type": bookData.type
        }
      }).then(
          (response) => {
            console.log(response)
            if (response.status == 200) {
              this.editMode[index] = false
            }
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
.fullScreenContainer {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: center;
}

.fullScreenImg {
  /*width: 100%;*/
  image-rendering: auto;
  height: 100vh;

}

.page_slider {
  width: calc(100% - 505px);
  margin-left: 20px;
}

.el-switch {
  margin-left: 20px;
}

</style>
