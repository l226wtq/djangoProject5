<template>
  <div v-show="!fullScreenViewMode">
    <DxBox id="mainDxBox" direction="col" height="100%" width="100%">
      <DxItem :ratio="1" baseSize="5vh">
        <div style="font-size: 3vh">书籍查看管理</div>
      </DxItem>

      <DxItem :ratio="1" baseSize="93vh">
        <DxTabPanel
            id=""
            :swipeEnabled="true"
            :height="auto"
            :animationEnabled="false"
        >
          <DxItem title="信息管理列表" @click="clickDataGirdTitle">
            <book-data-grid-view
                v-model:bookObjects="bookObjects"
                ref="bookDataGrid"
            />
          </DxItem>
          <DxItem title="封面视图">
            <book-cover-view
                v-model:bookObjects="bookObjects"
                v-model:fullScreenViewMode="fullScreenViewMode"
                v-model:CurrentBookId="CurrentBookId"
                v-model:CurrentBookLength="CurrentBookLength"
            />
          </DxItem>
          <DxItem title="jxl显示测试">
            <!-- <div>什么都没有</div> -->
            <!--            <img src="http://127.0.0.1:8005/static/bookContent/21.jpg" ref="imgSrc">-->
            <!--            <img ref="imgResult"/>-->
            <!--            <button @click="compress">Compress!</button>-->
            <!--            <el-form ref="form" :model="form" label-width="120px" style="width: 50%">-->
            <!--              <el-form-item label="保存至文件夹">-->
            <!--                <input type="file" id="file" hidden @change="fileChange" webkitdirectory>-->
            <!--                <el-input placeholder="请输入内容" v-model="form.imgSavePath" class="input-with-select">-->
            <!--                  <template #append>-->
            <!--                    <el-button  type="success" @click="btnChange">打开文件夹</el-button>-->
            <!--                  </template>-->
            <!--                </el-input>-->
            <!--              </el-form-item>-->
            <!--            </el-form>-->

            <div v-for="(item) in 9">
              <span v-for="(item2) in item" style="width: 100px;display: inline-block">
                {{ item + '*' + item2 + '=' }}<span
                  :style="(item * item2) % 2 === 0 ?'color: red':'black'">{{ item * item2 }}</span>
              </span>
            </div>

            <textarea name="" id="" cols="100" rows="10">{{plusForm}}</textarea>
          </DxItem>
        </DxTabPanel>
      </DxItem>
    </DxBox>
  </div>
  <div v-if="fullScreenViewMode">
    <full-screen-view
        v-model:fullScreenViewMode="fullScreenViewMode"
        v-model:CurrentBookId="CurrentBookId"
        v-model:CurrentBookLength="CurrentBookLength"
    />
  </div>
</template>

<script>
import {DxBox, DxItem} from "devextreme-vue/box";
import DxTabPanel from "devextreme-vue/tab-panel";
import BookDataGridView from "./bookDataGridView.vue";
import BookCoverView from "./bookCoverView.vue";
import axios from "axios";
import FullScreenView from "./fullScreenView.vue";
import Pica from 'pica'

export default {
  name: "bookMainViewIndex",
  components: {
    DxBox,
    DxItem,
    DxTabPanel,
    BookDataGridView,
    BookCoverView,
    FullScreenView,
  },
  data() {
    return {
      bookObjects: [],
      fullScreenViewMode: false,
      CurrentBookId: 0,
      CurrentBookLength: 0,
      form: {
        imgSavePath: ''
      },
      plusForm: '1×1=1\n' +
          '1×2=2 2×2=4\n' +
          '1×3=3 2×3=6 3×3=9\n' +
          '1×4=4 2×4=8 3×4=12 4×4=16\n' +
          '1×5=5 2×5=10 3×5=15 4×5=20 5×5=25\n' +
          '1×6=6 2×6=12 3×6=18 4×6=24 5×6=30 6×6=36\n' +
          '1×7=7 2×7=14 3×7=21 4×7=28 5×7=35 6×7=42 7×7=49\n' +
          '1×8=8 2×8=16 3×8=24 4×8=32 5×8=40 6×8=48 7×8=56 8×8=64\n' +
          '1×9=9 2×9=18 3×9=27 4×9=36 5×9=45 6×9=54 7×9=63 8×9=72 9×9=81',
    };
  },
  created() {
    this.getAllbooksInfo();
  },
  methods: {
    fileChange(e) {
      try {
        const fu = document.getElementById('file')
        if (fu == null) return
        this.form.imgSavePath = fu.files[0].path
        console.log(fu.files[0].path)
      } catch (error) {
        console.debug('choice file err:', error)
      }
    },
    btnChange() {
      var file = document.getElementById('file')
      file.click()
    },
    compress() {
      const pica = Pica();

      const resizedCanvas = document.createElement("canvas");
      resizedCanvas.height = 20;
      resizedCanvas.width = 20;

      pica
          .resize(this.$refs.imgSrc, resizedCanvas)
          .then(result => {
            console.log("resize done!");
            this.$refs.imgResult.src = result.toDataURL();
          })
          .catch(error => {
            console.log("got error..");
            console.log(error);
          });
    },
    getAllbooksInfo() {
      console.log("获取所有书籍信息", this.bookObjects);
      axios
          .get("http://127.0.0.1:8005/book/")
          .then((response) => {
            // 处理成功情况
            this.bookObjects = response.data;
            console.log(response);
          })
          .catch((error) => {
            // 处理错误情况
            console.log(error);
          });
    },
    clickDataGirdTitle() {
      // console.log("clickDataGirdTitle", this.$refs.bookDataGrid);
      // this.$refs["test"].instance.refresh();
      // this.$refs.bookDataGrid.refreshDataGridSource();
    },
  },
};
</script>

<style>
</style>
