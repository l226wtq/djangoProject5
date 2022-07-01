<template>
  <div>
    <DxButton
      id=""
      text="新建采购入库单"
      type="default"
      styling-mode="outlined"
      icon="add"
      hint=""
      @click="addForm"
    />
    <DxPopup
      :width="900"
      :height="600"
      :visible="popupVisble"
      :show-title="true"
      title="新建采购入库单"
      :close-on-outside-click="false"
      :onShowing="getGoodsNumsList"
    >
      <template #content>
        <DxScrollView width="100%" height="100%">
          <DxForm
            id="form"
            :form-data="housingData"
            label-mode="outside"
            label-location="left"
            col-count="3"
          >
            <DxSimpleItem data-field="yundan" isRequired="True">
              <DxLabel text="运单号" />
            </DxSimpleItem>
            <DxSimpleItem
              data-field="gongyinshang"
              editorType="dxSelectBox"
              :editor-options="{
                items: supplierList,
                placeholder: '请选择供应商',
              }"
              isRequired="True"
            >
              <DxLabel text="供应商" />
            </DxSimpleItem>
            <DxSimpleItem data-field="shifujinge" isRequired="True">
              <DxLabel text="实付金额" />
            </DxSimpleItem>
            <DxSimpleItem
              data-field="shouhuoriqi"
              editorType="dxDateBox"
              isRequired="True"
            >
              <DxLabel text="收货日期" />
            </DxSimpleItem>
            <DxSimpleItem
              data-field="shouhuoriqi"
              :editor-options="{ disabled: true, placeholder: '自动生成计算' }"
            >
              <DxLabel text="合计金额" />
            </DxSimpleItem>
            <DxSimpleItem
              data-field="shouhuoriqi"
              :editor-options="{ disabled: true, placeholder: '自动生成计算' }"
            >
              <DxLabel text="大写金额" />
            </DxSimpleItem>
            <DxSimpleItem data-field="beizhu" :col-span="3">
              <DxLabel text="备注" />
            </DxSimpleItem>
          </DxForm>
          <hr />
          <div>入库明细</div>
          <DxDataGrid
            :data-source="housingData.itemsDataSource"
            key-expr="ID"
            :show-borders="true"
          >
            <DxEditing
              :allow-updating="true"
              :allow-adding="true"
              :allow-deleting="true"
              mode="row"
            />
            <DxColumn data-field="number" caption="货品编码">
              <DxLookup :data-source="GoodsNumsList" />
            </DxColumn>
            <DxColumn data-field="type" caption="货品类别" />
            <DxColumn data-field="name" caption="货品名称" />
            <DxColumn data-field="specification" caption="规格型号" />
            <DxColumn data-field="unit" caption="单位" />
            <DxColumn data-field="price" caption="单价" />
            <DxColumn data-field="inventoryCount" caption="库存数量" />
            <DxColumn data-field="count" caption="数量" />
            <DxColumn data-field="totalPrice" caption="金额" />
          </DxDataGrid>
          <hr />
          <DxButton
            id=""
            text="提交"
            type="default"
            styling-mode="outlined"
            icon=""
            hint=""
            @click="submitForm($event)"
          />
        </DxScrollView>
      </template>
    </DxPopup>

    <hr />
    <div>采购入库单列表</div>
    <DxDataGrid
      :dataSource="inboundJournalList"
      :filter-value="['journalType', '=', '采购入库']"
    >
      <DxColumn
        v-for="(value, key, index) in inboundJournalListColumn"
        :key="index"
        :data-field="value"
        :caption="key"
        :columns-auto-width="true"
      />
      <!-- <DxFilterRow :visible="true" /> -->
      <!-- <DxFilterPanel :visible="true" /> -->
      <DxHeaderFilter :visible="true" />
    </DxDataGrid>
  </div>
</template>

<script>
import DxButton from "devextreme-vue/button";
import { DxPopup, DxPosition, DxToolbarItem } from "devextreme-vue/popup";
import { DxScrollView } from "devextreme-vue/scroll-view";
import {
  DxForm,
  DxSimpleItem,
  DxLabel,
  DxEmptyItem,
} from "devextreme-vue/form";
import {
  DxDataGrid,
  DxColumn,
  DxGrouping,
  DxGroupPanel,
  DxEditing,
  DxPager,
  DxPaging,
  DxSearchPanel,
  DxToolbar,
  DxLookup,
  DxHeaderFilter,
  DxFilterRow,
  DxFilterPanel,
  DxFilterBuilderPopup,
} from "devextreme-vue/data-grid";
import axios from "axios";
export default {
  name: "PSIwarehousingPurchaseMainView",
  components: {
    DxButton,
    DxPopup,
    DxPosition,
    DxToolbarItem,
    DxScrollView,
    DxForm,
    DxSimpleItem,
    DxLabel,
    DxDataGrid,
    DxColumn,
    DxGrouping,
    DxEditing,
    DxGroupPanel,
    DxPager,
    DxPaging,
    DxSearchPanel,
    DxToolbar,
    DxLookup,
    DxEmptyItem,
    DxHeaderFilter,
    DxFilterRow,
    DxFilterPanel,
    DxFilterBuilderPopup,
  },
  data() {
    return {
      housingData: {
        yundan: "",
        gongyinshang: "",
        shifujinge: "",
        shouhuoriqi: "",
        beizhu: "",
        itemsDataSource: [
          {
            ID: 1,
            number: "",
            type: "",
            name: "",
            specification: "",
            unit: "",
            price: "",
            inventoryCount: "",
            count: "",
            totalPrice: "",
          },
        ],
      },
      popupVisble: false,
      inboundJournalListColumn: {
        业务日期: "date",
        单据类型: "journalType",
        单据编号: "journalNumber",
        货品编号: "number",
        货品类型: "type",
        货品名称: "name",
        规格型号: "specification",
        单位: "unit",
        入库数量: "inboundCount",
        入库金额: "inboundAmount",
        出库数量: "outboundCount",
        出库金额: "outboundAmount",
      },
      GoodsNumsList: [],
      supplierList: ["A", "B"],
      inboundJournalList: [],
    };
  },
  created() {
    this.getInboundJournalList();
  },
  methods: {
    addForm() {
      console.log("test");
      this.popupVisble = true;
    },
    reVisable() {
      this.popupVisble = false;
    },
    getGoodsNumsList() {
      console.log("here");
      axios
        .get("http://127.0.0.1:8000/genericviewgoodslist/numslist/")
        .then((response) => {
          // 处理成功情况
          this.GoodsNumsList = response.data;
          console.log(response);
        })
        .catch((error) => {
          // 处理错误情况
          console.log(error);
        });
    },
    getInboundJournalList() {
      axios
        .get("http://127.0.0.1:8000/genericviewboundjournallist/")
        .then((response) => {
          // 处理成功情况
          this.inboundJournalList = response.data;
          console.log("genericviewboundjournallist", response);
        })
        .catch((error) => {
          // 处理错误情况
          console.log(error);
        });
    },
    submitForm(event) {
      // console.log("转换", JSON.stringify(postTemp));
      axios
        .post("http://127.0.0.1:8000/genericviewboundjournallist/", {
          date: "1980-09-09",
          journalType: "in pariat",
          journalNumber: this.housingData.yundan,
          number: "35",
          type: "veniam nostrud anim",
          name: "存节江劳严经",
          specification: "dolor sint incididunt tempor",
          unit: "voluptate",
          inboundCount: 37,
          inboundAmount: 50,
          outboundCount: 57,
          outboundAmount: 42,
        })
        .then((response) => {
          // 处理成功情况
          this.inboundJournalList = response.data;
          console.log("genericviewboundjournallist", response);
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