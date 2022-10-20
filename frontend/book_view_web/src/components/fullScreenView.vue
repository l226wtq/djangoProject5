<template>
  <el-container id="fullScreenContentor">
    <el-main>
      <div class="img-box">
        <el-image
            id="LeftPic"
            ref="LeftPic"
            :src="viewPicUrlLeft"
            alt=""
            @click="lastPic"
            v-if="leftPicSwitch"
        />
        <el-image
            ref="RightPic"
            :src="viewPicUrlRight"
            alt=""
            @click="nextPic"
            v-if="rightPicSwitch"
        />
      </div>
    </el-main>
    <el-aside width="250px">
      <el-row>
        <el-button type="warning" @click="exitFullScreenView">返回</el-button>
      </el-row>
      <el-row>
        <el-button @click="enterFullScreen">进入全屏</el-button>
      </el-row>
      <el-row v-show="this.singlePageEnable">当前页数/总页数：{{ page }} / {{ CurrentBookLength }}</el-row>
      <el-row v-show="!this.singlePageEnable">当前页数/总页数：{{ page + 1 }} - {{ page }} / {{
          CurrentBookLength
        }}
      </el-row>
      <el-row>
        <el-button @click="switchSinglePageEnable">单页显示</el-button>
        <el-button @click="switchDualPageEnable">双页显示</el-button>
      </el-row>
      <el-row>
        <el-button @click="fixPageAdd">调整跨页+1</el-button>
        <el-button @click="fixPageSub">调整跨页-1</el-button>
      </el-row>
      <hr>
      <el-row>
        <el-col :span="4"><span>作者</span></el-col>
        <el-col :span="20">
          <el-input></el-input>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="4"><span>日期</span></el-col>
        <el-col :span="20">
          <el-date-picker></el-date-picker>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="4"><span>评分</span></el-col>
        <el-col :span="20">
          <el-rate size="large"></el-rate>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="4"><span>类型</span></el-col>
        <el-col :span="20">
          <el-select></el-select>
        </el-col>
      </el-row>
    </el-aside>

  </el-container>
</template>

<script>
const pica = require('pica')();


export default {
  name: "fullScreenView",
  props: {
    fullScreenViewMode: Boolean,
    CurrentBookId: Number,
    CurrentBookLength: Number,
  },
  data() {
    return {
      fullSize: {
        height: 0,
        width: 0,
      },
      singlePageEnable: false,
      page: 1,
    };
  },
  emit: [
    "update:fullScreenViewMode",
    "update:CurrentBookId",
    "update:CurrentBookLength",
  ],
  created() {
    // this.left = document.getElementById("LeftPic")?.offsetHeight;
  },
  methods: {

    enterFullScreen() {
      document.documentElement.requestFullscreen().catch((err) => {
        console.log(err)
      })
    },
    exitFullScreenView() {
      this.page = 1;
      this.$emit("update:fullScreenViewMode", false);
    },
    nextPic() {
      if (this.singlePageEnable) {
        if (this.page < this.CurrentBookLength) {
          this.page += 1;
        } else {
          alert("看完咯");
        }
      } else {
        if (this.page + 1 < this.CurrentBookLength) {
          this.page += 2;
        } else {
          alert("看完咯");
        }
      }
    },
    lastPic() {
      if (this.page > 1) {
        this.page -= 2;
      }
    },
    switchSinglePageEnable() {
      this.singlePageEnable = true;
    },
    switchDualPageEnable() {
      this.singlePageEnable = false;
    },
    fixPageAdd() {
      if (this.page > 1) {
        this.page += 1;
      }
    },
    fixPageSub() {

      this.page -= 1;
    },
  },
  computed: {
    viewPicUrlLeft() {
      console.log(
          "Left",
          this.CurrentBookId,
          this.CurrentBookLength,
          this.page + 1
      );
      return `http://127.0.0.1:8005/genericbook/zip/${
          this.CurrentBookId
      }&page=${this.page + 1}`;
    },
    viewPicUrlRight() {
      console.log(
          "right",
          this.CurrentBookId,
          this.CurrentBookLength,
          this.page
      );
      return `http://127.0.0.1:8005/genericbook/zip/${this.CurrentBookId}&page=${this.page}`;
    },
    leftPicSwitch() {
      if (this.page + 1 > this.CurrentBookLength || this.singlePageEnable) {
        return false;
      } else {
        return true;
      }
    },
    rightPicSwitch() {
      if (this.page > this.CurrentBookLength) {
        return false;
      } else {
        return true;
      }
    },
  },
};
</script>

<style>
body {
  margin: 0;
}

#fullScreenContentor {
  background-color: gray;
  height: 100vh;
}

#fullScreenContentor .el-main {
  padding: 0;
  height: 100%;
}

.img-box {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

#fullScreenContentor .el-image {
  height: 100%;
}

img {
  /*max-height: calc(98vh - 44px);*/
  image-rendering: high-quality;
}
</style>
