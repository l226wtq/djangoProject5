<template>
  <div>这是dbExportBackup界面</div>
  <DxButton
    id=""
    text="连接数据库"
    type="default"
    styling-mode="outlined"
    icon=""
    hint=""
    @click="onClick(event)"
  />
  <DxDataGrid
    id=""
    class="table-page"
    :show-borders="true"
    :data-source="datasourc"
    :remote-operations="true"
    :allow-column-resizing="true"
    :column-auto-width="true"
    :loadPanel="{ showIndicator: false, showPane: false, text: '' }"
    key-expr=""
    height="calc(100vh - )"
    @cellHoverChanged="onCellHoverChanged"
  >
    <DxPaging :page-size="20" />
    <DxScrolling mode="standard" row-rendering-mode="standard" />
    <DxColumnFixing :enabled="true" />
    <DxHeaderFilter :visible="true" />
    <DxFilterRow :visible="true" apply-filter="auto" />
    <DxSelection
      mode="multiple"
      show-check-boxes-mode="always"
      select-all-mode="allPages"
    />
    <DxColumn
      :allowFiltering="true"
      :allowSorting="true"
      :fixed="true"
      :header-filter="{ dataSource: dataSourceFilter }"
      format="HH:mm:ss dd/MM/yyyy"
      data-field=""
      caption=""
      width=""
      groupCellTemplate="groupCellTemplate"
      alignment="left"
    ></DxColumn>
    <!-- Summary -->
    <DxSummary>
      <DxGroupItem
        column=""
        summary-type="sum"
        display-format="{0} ..."
        :show-in-group-footer="true"
        :align-by-column="true"
        :customize-text="customizeSummary"
      />
    </DxSummary>
  </DxDataGrid>
</template>

<script>
import {
    DxScrolling,
    DxColumnFixing,
    DxSelection,
    DxSummary,
    DxGroupItem,
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
import DxButton from "devextreme-vue/button";
export default {
  name: "dbExportBackup",
  components: {
    DxScrolling,
    DxColumnFixing,
    DxSelection,
    DxSummary,
    DxGroupItem,
    DxButton,
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
  },
};
</script>

<style>
</style>