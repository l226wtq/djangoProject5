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
    :onInitNewRow="onInitNewRow"
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
      >
      </DxPopup>
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
            data-field="lastestSqlStatment"
            editor-type="dxTextArea"
          />

          <DxItem
            cssClass="popSqlExplanationTextArea"
            :col-span="4"
            :editor-options="{ height: 135 }"
            data-field="lastestSqlExplanation"
            editor-type="dxTextArea"
          />
          <DxItem data-field="enable" :col-span="1" />
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
    <DxColumn data-field="enable" caption="启用状态" data-type="boolean">
    </DxColumn>
    <DxColumn
      data-field="lastestSqlStatment"
      caption="SQL语句"
      width="45%"
      cellTemplate="sqlStatmentTextArea"
    />
    <template #sqlStatmentTextArea="{ data: dataObj }">
      <div class="sqlStatmentTextArea">
        <highlightjs
          id="sqlHljs"
          language="sql"
          :code="dataObj.value"
          style="width: calc(100% - 50px)"
        />
        <div id="viewButtonGroup">
          <DxButton
            icon="copy"
            text="复制SQL"
            v-clipboard:copy="dataObj.value"
            style="width: 150px"
          />
          <DxButton
            icon="comment"
            text="查看SQL记录"
            style="width: 150px"
            @click="viewSqlsPopup(event, dataObj)"
          >
          </DxButton>
        </div>
      </div>
    </template>
    <DxColumn
      data-field="lastestSqlExplanation"
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
        :value="dataObj.value"
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
  <DxPopup
    v-model:visible="popupVisible"
    :dragEnabled="true"
    :show-close-button="true"
    :show-title="true"
    :width="1280"
    :height="760"
    title="sql记录"
  >
    <DxDataGrid
      id=""
      class="table-page"
      :show-borders="true"
      :show-row-lines="true"
      :data-source="sqls"
      :allow-column-resizing="true"
      :column-auto-width="true"
      height="calc(100vh - )"
      no-data-text="无数据"
      @cellHoverChanged="onCellHoverChanged"
    >
      <DxPaging :page-size="5" />
      <DxEditing
        :allow-updating="false"
        :allow-deleting="false"
        :allow-adding="false"
        mode="row"
      />
      <DxScrolling mode="standard" row-rendering-mode="standard" />
      <DxColumnFixing :enabled="true" />
      <DxHeaderFilter :visible="true" />
      <!-- <DxFilterRow :visible="true" apply-filter="auto" /> -->
      <DxColumn data-field="id" caption="ID(倒序)" alignment="left" width="90px"> </DxColumn>
      <DxColumn
        data-field="sqlStatment"
        caption="sql语句记录"
        alignment="left"
        cellTemplate="sqlStatmentDetailsTextArea"
      ></DxColumn>
      <template #sqlStatmentDetailsTextArea="{ data: dataObj }">
        <highlightjs id="sqlHljs" language="sql" :code="dataObj.value" />
      </template>
      <DxColumn
        data-field="sqlExplanation"
        caption="sql注释说明记录"
        alignment="left"
        cellTemplate="sqlStatmentExplanationDetailsTextArea"
      ></DxColumn>
      <template #sqlStatmentExplanationDetailsTextArea="{ data: dataObj }">
        <!-- <p name="" id="ss" class="ss" readonly>
        {{ dataObj.data.sqlExplanation }}
      </p> -->
        <DxTextArea
          :autoResizeEnabled="true"
          :minHeight="50"
          :maxHeight="300"
          id="sqlStatmentExplanationTextArea"
          :value="dataObj.value"
          placeholder="SQL语句说明"
          :readOnly="true"
        />
      </template>
      <!-- Summary -->
    </DxDataGrid>
  </DxPopup>
</template>

<script>
import { DxPopup, DxPosition, DxToolbarItem } from "devextreme-vue/popup";
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
  DxForm,
  DxRequiredRule,
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
    DxRequiredRule,
  },

  data() {
    return {
      sqlStatments: [
        {
          id: 0,
          name: "0",
          sysType: "1",
          tpye: "",
          enable: true,
          lastestSqlStatment: "",
          lastestSqlExplanation: "",
        },
      ],
      sqls: [{ id: 0, sqlStatment: "", sqlExplanation: "" }],
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
    onInitNewRow(e) {
      console.log("onInitNewRow", e);
      e.data.enable = true;  //默认值为true
      if (this.$route.params.sysType != undefined) {
        e.data.sysType=this.$route.params.sysType;
      } else {
        console.log("$route.params={}", this.$route.params.sysType);
        return "";
      }
    },
    add(e) {
      console.log("add", e);
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
    getSqls(id) {
      axios
        .get(`http://127.0.0.1:8000/genericviewsqlstatment/${id}/`)
        .then((response) => {
          // 处理成功情况
          this.sqls = response.data;
          console.log("getSqls", response);
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
      console.log("afterRowUpdate", event, this.sqlStatments);
      this.updateSqlDocument(event.data);
    },
    updateSqlDocument(updateData) {
      console.log("updateData", updateData);
      axios
        .put(
          `http://127.0.0.1:8000/genericviewsqlstatment/${updateData.id}/`,
          updateData
        )
        .then((response) => {
          // 处理成功情况
          console.log("after genericviewsqlstatment", response);
        })
        .catch((error) => {
          // 处理错误情况
          console.log(error);
        });
    },
    viewSqlsPopup(event, obj) {
      console.log("点击了viewSqlsPopup", event, obj.data.id);
      this.popupVisible = !this.popupVisible;
      this.getSqls(obj.data.id);
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

#viewButtonGroup {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>