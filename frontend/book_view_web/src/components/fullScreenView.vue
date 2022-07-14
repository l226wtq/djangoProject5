<template>
  <div class="fullScreenContentor">
    <div>
      header-{{ page }}-{{ CurrentBookLength }}
      <button :onclick="exitFullScreenView">返回</button>
    </div>
    <div class="fullScreenViewBody">
      <div class="img-box">
        <img
          id="LeftPic"
          ref="LeftPic"
          :src="viewPicUrlLeft"
          alt=""
          :onclick="lastPic"
          v-if="leftPicSwitch"
        />
        <img
          ref="RightPic"
          :src="viewPicUrlRight"
          alt=""
          :onclick="nextPic"
          v-if="rightPicSwitch"
        />
      </div>
    </div>
    <!-- <div>
      footer
      <button :onclick="nextPic">切换图片</button>
    </div> -->
  </div>
</template>

<script>
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
    exitFullScreenView() {
      this.page = 1;
      this.$emit("update:fullScreenViewMode", false);
    },
    nextPic() {
      if (this.page < this.CurrentBookLength) {
        this.page += 2;
      }
    },
    lastPic() {
      if (this.page > 1) {
        this.page -= 2;
      }
    },
  },
  data() {
    return {
      page: 1,
    };
  },
  computed: {
    viewPicUrlLeft() {
      console.log(
        "Left",
        this.CurrentBookId,
        this.CurrentBookLength,
        this.page + 1
      );
      return `http://127.0.0.1:8000/genericbook/zip/${
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
      return `http://127.0.0.1:8000/genericbook/zip/${this.CurrentBookId}&page=${this.page}`;
    },
    leftPicSwitch() {
      if (this.page + 1 > this.CurrentBookLength) {
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
.fullScreenContentor {
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;
  height: 98vh;
  border-style: solid;
  border-width: 2px;
  background-color: gray;
}

.img-box {
  display: flex;
  align-items: center;
  justify-content: center;
}

img {
  max-height: calc(98vh - 44px);
  image-rendering: -webkit-optimize-contrast;
  image-rendering: crisp-edges;
}
</style>