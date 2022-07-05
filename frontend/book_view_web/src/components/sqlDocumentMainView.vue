<template>
  <DxDataGrid
    ref="tool"
    class="table-page"
    :show-borders="true"
    :show-row-lines="true"
    :dataSource="sqlStatments"
    :allow-column-resizing="true"
    :column-auto-width="true"
    :filterValue="datagridFilter"
    key-expr="id"
    :onRowInserted="afterAddRow"
    :onRowUpdated="afterRowUpdate"
  >
    <DxPaging :page-size="10" />
    <DxPager
      :visible="true"
      :show-page-size-selector="true"
      :show-info="true"
      :show-navigation-buttons="true"
    />
    <DxEditing
      :allow-updating="true"
      :allow-deleting="false"
      :allow-adding="true"
      mode="popup"
    >
      <DxPopup
        :show-title="true"
        :width="1280"
        :height="820"
        title="新建SQL文档"
      />
      <DxForm :col-count="4">
        <DxItem :col-count="4" :col-span="4" item-type="group">
          <DxItem data-field="name" :col-span="4" />
          <DxItem data-field="type" :col-span="2" />
          <DxItem data-field="sysType" :col-span="2" />
        </DxItem>

        <DxItem
          :col-count="4"
          :col-span="4"
          item-type="group"
          caption="SQL定义"
        >
          <DxItem
            cssClass="popSqlStatmentTextArea"
            :col-span="4"
            :editor-options="{ height: 300 }"
            data-field="sqlStatment"
            editor-type="dxTextArea"
          />

          <DxItem
            cssClass="popSqlExplanationTextArea"
            :col-span="4"
            :editor-options="{ height: 150 }"
            data-field="sqlExplanation"
            editor-type="dxTextArea"
          />
          <DxItem
            data-field="enable"
            :col-span="1"
            editor-type="dxCheckBox"
            :editor-options="checkBoxOptions"
          />
        </DxItem>
      </DxForm>
    </DxEditing>

    <DxColumn data-field="id" caption="ID" data-type="number" width="2%" />
    <DxColumn
      data-field="name"
      caption="SQL语句名称"
      width="13%"
      data-type="string"
    />
    <DxColumn
      data-field="sysType"
      caption="SQL所属系统"
      width="6%"
      data-type="string"
    >
      <DxLookup
        :data-source="sysTypeDefine"
        value-expr="type"
        display-expr="displayName"
      >
      </DxLookup>
    </DxColumn>
    <DxColumn
      data-field="type"
      width="6%"
      caption="SQL操作类型"
      data-type="string"
    >
      <DxLookup
        :data-source="typeDefine"
        value-expr="type"
        display-expr="displayName"
      >
      </DxLookup>
    </DxColumn>
    <DxColumn
      data-field="enable"
      width="5%"
      caption="启用状态"
      data-type="boolean"
    />
    <DxColumn
      data-field="sqlStatment"
      caption="SQL语句"
      width="45%"
      cellTemplate="sqlStatmentTextArea"
      data-type="string"
    />
    <template #sqlStatmentTextArea="{ data: dataObj }">
      <div class="sqlStatmentTextArea">
        <!-- <DxTextArea
          :height="100"
          :max-length="1000"
          v-model:value="dataObj.data.sqlStatment"
          placeholder="SQL语句"
          :readOnly="true"
          style="width: calc(100% - 0px)"
        >
        </DxTextArea> -->
        <highlightjs
          id="sqlHljs"
          language="sql"
          :code="dataObj.data.sqlStatment"
          style="width: calc(100% - 50px)"
        />

        <DxButton
          icon="copy"
          v-clipboard:copy="dataObj.data.sqlStatment"
          style="width: 50px"
        />
      </div>
    </template>
    <DxColumn
      data-field="sqlExplanation"
      width="23%"
      caption="SQL注释说明"
      cellTemplate="sqlStatmentExplanationTextArea"
      data-type="string"
    />
    <!-- <DxTextArea
      id="inputZhehang"
      height='inherit'
        v-model:value="dataObj.data.sqlExplanation"
        placeholder="SQL语句说明"
        :readOnly="true"
      /> -->
    <template #sqlStatmentExplanationTextArea="{ data: dataObj }">
      <!-- <p name="" id="ss" class="ss" readonly>
        {{ dataObj.data.sqlExplanation }}
      </p> -->
      <DxTextArea
        :autoResizeEnabled="true"
        :minHeight="50"
        :maxHeight="300"
        id="sqlStatmentExplanationTextArea"
        v-model:value="dataObj.data.sqlExplanation"
        placeholder="SQL语句说明"
        :readOnly="true"
      />
    </template>
    <DxToolbar>
      <!-- <DxItem location="before">
        <DxButton @click="addSqlRowInfo()" icon="add" text="新建一条SQL信息" />
      </DxItem> -->
      <DxItem location="before">
        <DxButton @click="add($event)" icon="add" text="新建一条SQL信息" />
      </DxItem>
      <!-- <DxItem location="after">
        <DxButton icon="trash" text="删除选中的SQL信息" />
      </DxItem> -->
    </DxToolbar>
  </DxDataGrid>
</template>

<script>
// import { DxPopup, DxPosition, DxToolbarItem } from "devextreme-vue/popup";
import DxButton from "devextreme-vue/button";
import {
  DxPaging,
  DxPager,
  DxScrolling,
  DxColumnFixing,
  DxHeaderFilter,
  DxFilterRow,
  DxSelection,
  DxSummary,
  DxGroupItem,
  DxDataGrid,
  DxColumn,
  DxEditing,
  DxToolbar,
  DxItem,
  DxLookup,
  DxPopup,
  DxForm,
} from "devextreme-vue/data-grid";
import DxTextArea from "devextreme-vue/text-area";
import axios from "axios";
export default {
  name: "sqlDocumentMainView",
  components: {
    DxLookup,
    DxPaging,
    DxPager,
    DxScrolling,
    DxColumnFixing,
    DxHeaderFilter,
    DxFilterRow,
    DxSelection,
    DxSummary,
    DxGroupItem,
    DxButton,
    DxDataGrid,
    DxColumn,
    DxEditing,
    DxLookup,
    DxTextArea,
    DxToolbar,
    DxItem,
    DxPopup,
    DxForm,
  },

  data() {
    return {
      sqlStatments: [
        {
          id: 0,
          name: "0",
          sysType: "",
          tpye: "",
          enable: false,
          sqlStatment: "",
          sqlExplanation: "",
        },
      ],
      popupVisible: false,
      typeDefine: [
        { type: "sear", displayName: "搜索" },
        { type: "up", displayName: "更新" },
        { type: "a", displayName: "新增" },
        { type: "rem", displayName: "移除" },
      ],
      sysTypeDefine: [
        { type: "xiaoshou", displayName: "销售" },
        { type: "renshi", displayName: "人事" },
        { type: "kaoqing", displayName: "考勤" },
      ],
      checkBoxOptions: { value: true },
    };
  },
  computed: {
    datagridFilter() {
      if (this.$route.params.sysType != undefined) {
        return ["sysType", "=", this.$route.params.sysType];
        console.log("$route.params111", this.$route.params.sysType);
      } else {
        console.log("$route.params={}", this.$route.params.sysType);
        return "";
      }
    },
  },
  created() {
    this.getsqlDocument();
  },
  methods: {
    add(e) {
      console.log(e);
      this.$refs.tool.instance.addRow();
    },
    afterAddRow(event) {
      console.log("添加了一行", event);
      this.submitSqlDocument(event.data);
    },
    getsqlDocument() {
      axios
        .get("http://127.0.0.1:8000/genericviewsqlstatment/")
        .then((response) => {
          // 处理成功情况
          this.sqlStatments = response.data;
          console.log("genericviewsqlstatment", response);
        })
        .catch((error) => {
          // 处理错误情况
          console.log(error);
        });
    },
    submitSqlDocument(postData) {
      console.log("postData", postData, this.sqlStatments);
      axios
        .post("http://127.0.0.1:8000/genericviewsqlstatment/", postData)
        .then((response) => {
          // 处理成功情况
          console.log("after genericviewsqlstatment", response);
          this.sqlStatments[this.sqlStatments.length - 1].id = response.data.id;
          console.log(
            "lastone",
            this.sqlStatments[this.sqlStatments.length - 1]
          );
        })
        .catch((error) => {
          // 处理错误情况
          console.log(error);
        });
    },
    afterRowUpdate(event) {
      console.log("afterRowUpdate", event);
      this.updateSqlDocument(event.data);
    },
    updateSqlDocument(updateData) {
      console.log("updateData", updateData);
      axios
        .put(`http://127.0.0.1:8000/genericviewsqlstatment/${updateData.id}/`, updateData)
        .then((response) => {
          // 处理成功情况
          console.log("after genericviewsqlstatment", response);
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
.table-page {
  height: 80vh;
}
.sqlStatmentTextArea {
  display: flex;
}

.popSqlStatmentTextArea textarea,
.popSqlExplanationTextArea textarea {
  white-space: nowrap !important;
}

#sqlHljs {
  padding: 0px;
  margin: 0px;
  min-height: 50px;
  max-height: 300px;
  overflow: auto;
}

#sqlStatmentExplanationTextArea {
  border-style: hidden;
}
</style>