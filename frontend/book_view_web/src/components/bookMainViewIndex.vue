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
            <img src="http://127.0.0.1:8005/static/bookContent/0001.jxl" alt="">
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
import { DxBox, DxItem } from "devextreme-vue/box";
import DxTabPanel from "devextreme-vue/tab-panel";
import BookDataGridView from "./bookDataGridView.vue";
import BookCoverView from "./bookCoverView.vue";
import axios from "axios";
import FullScreenView from "./fullScreenView.vue";
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
    };
  },
  created() {
    this.getAllbooksInfo();
  },
  methods: {
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
