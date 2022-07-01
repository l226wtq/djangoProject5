<template>
  <DxDataGrid
    :data-source="bookObjects"
    :show-borders="true"
    ref="test"
    :onRowRemoving="onRowRemoving"
    :onSaving="onSaving"
  >
    <DxEditing
      :allow-adding="true"
      :allow-updating="true"
      :allow-deleting="true"
      mode="cell"
    />
    <!-- 选择框多选模式 -->
    <DxSelection mode="multiple" />
    <DxColumn data-field="id" caption="顺序" alignment="center" />
    <DxColumn data-field="title" caption="标题" alignment="center" />
    <DxColumn data-field="author" caption="作者" alignment="center" />
    <DxColumn data-field="publishDate" caption="出版时间" alignment="center" />
    <DxColumn data-field="rating" caption="评分" alignment="center" />
    <DxColumn data-field="type" caption="类型" alignment="center" />
    <DxToolbar>
      <DxItem name="addRowButton" :show-text="true" />
      <DxItem location="after">
        <DxButton icon="trash" text="删除已选择的行数据" />
      </DxItem>
    </DxToolbar>
    <DxPaging :page-size="20" />
    <DxPager
      :visible="true"
      :show-page-size-selector="true"
      :allowed-page-sizes="[20, 30]"
      :show-navigation-buttons="true"
      :show-info="true"
    />
  </DxDataGrid>
</template>

<script>
import { DxBox, DxItem } from "devextreme-vue/box";
import {
  DxDataGrid,
  DxColumn,
  DxPager,
  DxPaging,
  DxEditing,
  DxSelection,
  DxToolbar,
} from "devextreme-vue/data-grid";
import { DxButton } from "devextreme-vue/button";
import axios from "axios";
export default {
  name: "bookDataGridView",
  components: {
    DxBox,
    DxItem,
    DxDataGrid,
    DxColumn,
    DxPaging,
    DxPager,
    DxEditing,
    DxSelection,
    DxToolbar,
    DxButton,
  },
  props: {
    bookObjects:Array,
  },
  data() {
    return {
    };
  },
  created() {
    // this.getAllbooksInfo();
    console.log(this.bookObjects)
  },
  methods: {
    // getAllbooksInfo() {
    //   console.log("获取所有书籍信息", this.bookObjects);
    //   axios
    //     .get("http://127.0.0.1:8000/book/")
    //     .then((response) => {
    //       // 处理成功情况
    //       this.bookObjects = response.data;
    //       console.log(response);
    //     })
    //     .catch((error) => {
    //       // 处理错误情况
    //       console.log(error);
    //     });
    // },
    onRowRemoving(e) {
      console.log("bookRowRemoving", e.data.id);
      axios
        .delete(`http://127.0.0.1:8000/book/${e.data.id}/`)
        .then((response) => {
          console.log("已成功发送删除", response);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    onSaving(e) {
      console.log("触发onSaving", e);
      if (e.changes[0].type == "update") {
        // const updatedData = Object.assign(e.changes[0].key, e.changes[0].data);
        // console.log(updatedData);
        axios
          .put(
            `http://127.0.0.1:8000/book/${e.changes[0].key.id}/`,
            e.changes[0].data
          )
          .then((response) => {
            console.log("已成功发送更新", response);
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
  },
};
</script>

<style>
</style>