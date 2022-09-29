<template>
  <DxBox id="coverDxBox" direction="row" height="100%" width="100%">
    <DxItem :ratio="1">
      <div id="CoverItems" class="CoverItemList">
        <div
          v-for="(item, index) in bookObjects"
          :key="index"
          class="singleCoverItem"
        >
          <!-- <div class="CoverItemsHeader1">
            <div class="CoverItemText">{{ item.title }}</div>
          </div>
          <div class="CoverItemsHeader2">
            <div class="CoverItemText">{{ item.author }}</div>
            <div class="CoverItemText">{{ item.publishDate }}</div>
          </div>
          <div class="CoverItemsHeader3">
            <div class="CoverItemText">{{ item.rating }}</div>
            <div class="CoverItemText">{{ item.type }}</div>
          </div> -->
          <!-- <div>{{ (index, editDisable) }}{{ editDisable[index] }}</div> -->
          <el-row>
            <el-col :span="24">
              <el-input
                v-model="item.title"
                clearable
                :disabled="getDisableList(index)"
                noShadow
            /></el-col>
          </el-row>
          <div class="CoverItemsBody">
            <!-- <img
              :src="`http://127.0.0.1:8000/static/bookzips/covers/${item.id}.jpg`"
              alt="cover"
              class="coverPic"
              @click="openFullScreenView(item.id)"
            /> -->
            <el-image
              :src="`http://127.0.0.1:8005/static/bookzips/covers/${item.id}.webp`"
              class="coverPic"
              fit="contain"
              @click="openFullScreenView(item.id)"
            />
          </div>
          <el-row>
            <el-col :span="12"
              ><el-input
                v-model="item.author"
                clearable
                :disabled="getDisableList(index)"
                noShadow
            /></el-col>
            <el-col :span="12">
              <!-- <el-input
                v-model="item.publishDate"
                clearable
                :disabled="getDisableList(index)"
                noShadow
            /> -->
              <el-date-picker
                class="cover-date-picker"
                v-model="item.publishDate"
                type="date"
                placeholder="选择日期"
                size="default"
                value-format="YYYY-MM-DD"
                :disabled="getDisableList(index)"
                @change="pickedDate"
              />
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12"
              ><el-rate v-model="item.rating" :disabled="getDisableList(index)"
            /></el-col>
            <el-col :span="12">
              <!-- <el-input
                v-model="item.type"
                clearable
                :disabled="getDisableList(index)"
                noShadow
            /> -->
              <el-select
                v-model="item.type"
                class="m-2"
                placeholder="选择类型"
                :disabled="getDisableList(index)"
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
              @click="clickEditButton(item, index)"
              v-show="editDisable[index]"
              >编辑</el-button
            >
            <el-button
              type="warning"
              @click="clickSaveButton(item, index)"
              v-show="!editDisable[index]"
              >保存</el-button
            >
            <el-popconfirm
              title="确定要删除吗?"
              confirm-button-text="确认"
              cancel-button-text="手滑了"
              @confirm="deleteSingleBook(item, index)"
            >
              <template #reference>
                <el-button type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </el-row>
        </div>
      </div>
    </DxItem>
  </DxBox>
</template>

<script>
import { DxButton } from "devextreme-vue/button";
import { DxBox, DxItem } from "devextreme-vue/box";
import axios from "axios";
import { ref } from "vue";
import { isArray } from "@vue/shared";

const value1 = ref(null);
export default {
  name: "bookCoverView",
  components: {
    DxButton,
    DxBox,
    DxItem,
  },
  props: {
    bookObjects: Array,
    fullScreenViewMode: Boolean,
    CurrentBookId: Number,
    CurrentBookLength: Number,
  },
  created() {
    // this.initcallback();
  },
  data() {
    return {
      ratingValue: 3,
      editDisable: [],
      uneditedBookItem: "",
      bookType: ["连载漫画", "完结漫画"],
    };
  },
  emits: [
    "update:fullScreenViewMode",
    "update:CurrentBookId",
    "update:CurrentBookLength",
  ],

  methods: {
    // initcallback() {
    //   for (let i in this.bookObjects) {
    //     this.editDisable[i] =
    //       this.editDisable[i] == null ? true : this.editDisable[i];
    //   }
    // },
    getDisableList(index) {
      // console.log(index, this.editDisable[index]);
      if (this.editDisable[index] == undefined) {
        this.editDisable[index] = true;
      }
      return this.editDisable[index];
    },
    openFullScreenView(id) {
      console.log("点击了图片", this.fullScreenViewMode);
      this.$emit("update:fullScreenViewMode", true);
      this.$emit("update:CurrentBookId", id);
      //   console.log("点击的id", id, "CurrentBookId", this.CurrentBookId);
      this.getBookZipInfoLength(id);
    },
    getBookZipInfoLength(id) {
      axios
        .get(`http://127.0.0.1:8005/genericbook/zip/${id}/`)
        .then((response) => {
          console.log("getBookZipInfoLength", response);
          this.$emit("update:CurrentBookLength", response.data);
        })
        .catch((response) => {
          console.log(response);
        });
    },
    putSingleBookInfo(putItem) {
      console.log("putSingleBookInfo", putItem);
      axios
        .put(`http://127.0.0.1:8005/genericbook/${putItem.id}/`, putItem)
        .then((response) => {
          console.log("已成功发送更新", response);
        })
        .catch((response) => {
          console.log(response);
        });
    },
    deleteSingleBookInfo(deleItem) {
      console.log("deleteSingleBookInfo", deleItem);
      axios
        .delete(`http://127.0.0.1:8005/book/${deleItem.id}/`)
        .then((response) => {
          console.log("已成功发送删除", response);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    clickEditButton(item, index) {
      // this.editDisable[i] = false;
      console.log("clickEditButton", item);
      this.editDisable[index] = false;
      this.uneditedBookItem = JSON.stringify(item);
      console.log(this.uneditedBookItem);
    },
    clickSaveButton(changedItem, index) {
      console.log("clickSaveButton", changedItem);
      console.log(
        "stringify",
        this.uneditedBookItem == JSON.stringify(changedItem)
      );
      if (this.uneditedBookItem != JSON.stringify(changedItem)) {
        //item有修改的时候
        this.putSingleBookInfo(changedItem);
      } else {
        console.log("item没有修改");
      }
      // this.editDisable = true;
      // this.putSingleBookInfo(changedItem);
      this.editDisable[index] = true;
    },
    deleteSingleBook(item, index) {
      this.bookObjects.splice(index, 1);
      console.log(this.bookObjects);
      this.deleteSingleBookInfo(item);
    },
    pickedDate(e) {
      console.log("pickedDate", typeof e, e);
    },
  },
};
</script>

<style>
#CoverItems.CoverItemList {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row !important;
  justify-content: space-evenly;
  overflow-y: scroll;
}

.singleCoverItem {
  max-height: 450px;
  width: 260px;
  margin: 10px;
  border-style: solid;
  border-width: 1px;
}

#CoverItems .CoverItemsHeader1,
#CoverItems .CoverItemsHeader2,
#CoverItems .CoverItemsHeader3,
.CoverItemsBody {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
}
.CoverItemText {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.coverPic {
  max-height: 300px;
  object-fit: contain;
}
.el-input.is-disabled .el-input__inner[noShadow] {
  color: black;
}

.cover-date-picker {
  width: 100% !important;
}
</style>
