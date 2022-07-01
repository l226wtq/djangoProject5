<template>
  <h3>货品库存列表</h3>
  <DxDataGrid
    class="table-page"
    :show-borders="true"
    :data-source="goodsIntentoryData"
    :height="300"
  >
    <DxSearchPanel :visible="true" placeholder="搜索表内任意字段" />
    <DxFilterRow :visible="true" apply-filter="onClick" />
    <DxPaging :page-size="5" />
    <DxPager
      :visible="true"
      :show-page-size-selector="true"
      :allowed-page-sizes="[5, 10, 'all']"
      :show-navigation-buttons="true"
      :show-info="true"
    />
    <DxColumn
      v-for="(value, key, index) in goodsIntentoryColumn"
      :key="index"
      :data-field="value"
      :caption="key"
    />
  </DxDataGrid>
  <hr />
  <h3>商品列表</h3>
  <DxDataGrid
    class="table-page"
    :show-borders="true"
    :data-source="goodsListData"
    :height="300"
  >
    <DxSearchPanel :visible="true" placeholder="搜索表内任意字段" />
    <DxFilterRow :visible="true" apply-filter="onClick" />
    <DxPaging :page-size="5" />
    <DxPager
      :visible="true"
      :show-page-size-selector="true"
      :allowed-page-sizes="[5, 10, 'all']"
      :show-navigation-buttons="true"
      :show-info="true"
    />
    <DxColumn
      v-for="(value, key, index) in goodsListColumn"
      :key="index"
      :data-field="value"
      :caption="key"
    />
  </DxDataGrid>
</template>

<script>
import {
  DxDataGrid,
  DxColumn,
  DxGrouping,
  DxGroupPanel,
  DxPager,
  DxPaging,
  DxSearchPanel,
  DxFilterRow,
} from "devextreme-vue/data-grid";
import gridData from "..//static/data.json";
import axios from "axios";
export default {
  name: "PSImainListView",
  components: {
    DxDataGrid,
    DxColumn,
    DxGrouping,
    DxGroupPanel,
    DxPager,
    DxPaging,
    DxSearchPanel,
    DxFilterRow,
  },
  data() {
    return {
      goodsIntentoryColumn: {
        货品编号: "number",
        货品类别: "type",
        货品名称: "name",
        规格型号: "specification",
        单位: "unit",
        库存数量: "inventoryQuantity",
      },
      goodsListColumn: {
        货品类别: "type",
        货品编号: "number",
        货品名称: "name",
        规格型号: "specification",
        单位: "unit",
        货品图片: "pic",
        参考进价: "purchasePrice",
        参考售价: "sellingPrice",
        最低库存: "minInventoryQuantity",
        最高库存: "maxInventoryQuantity",
        备注: "remark",
      },
      goodsIntentoryData: [],
      goodsListData: [],
    };
  },
  created() {
    this.getGoodsIntentoryData();
    this.getGoodsListData();
  },
  methods: {
    getGoodsIntentoryData() {
      axios
        .get("http://127.0.0.1:8000/genericviewgoodsintentory/")
        .then((response) => {
          // 处理成功情况
          this.goodsIntentoryData = response.data;
          console.log(response);
        })
        .catch((error) => {
          // 处理错误情况
          console.log(error);
        });
    },
    getGoodsListData() {
      axios
        .get("http://127.0.0.1:8000/genericviewgoodslist/")
        .then((response) => {
          // 处理成功情况
          this.goodsListData = response.data;
          console.log(response);
        })
        .catch((error) => {
          // 处理错误情况
          console.log(error);
        });
    },
  },
};
</script>

<style>
</style>