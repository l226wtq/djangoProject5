<template>
  <div class="common-layout">
    <el-container>
      <el-main>
        <el-tabs v-model="activeName" class="demo-tabs" type="card">
          <el-tab-pane label="LibPath&settings" name="libsetting">
            <lib-settings/>
          </el-tab-pane>
          <el-tab-pane label="ListView" name="second">ListView</el-tab-pane>
          <el-tab-pane label="thumbnailView" name="third">
            <thumbnail-view/>
          </el-tab-pane>
          <el-tab-pane label="reserved" name="fourth">Reserved</el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import libSettings from "@/components/comicTabComponents/lib&settings";
import ThumbnailView from "@/components/comicTabComponents/thumbnailView";

export default {
  name: "comicManager",
  components: {ThumbnailView, libSettings},
  data() {
    return {
      activeName: 'libsetting'
    }
  }
}
</script>

<style scoped>
.el-main {
  --el-main-padding: 0px;
  height: 100vh
}
</style>
