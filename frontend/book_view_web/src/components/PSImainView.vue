 <template id="view-container">
  <DxBox height="100%" direction="col" width="100%">
    <DxItem :ratio="0" :base-size="80">
      <template #default>
        <div
          style="
            background-color: skyblue;
            font-size: 18px;
            text-align: center;
            line-height: 80px;
          "
        >
          进销存PSI系统
        </div>
      </template>
    </DxItem>
    <DxItem :ratio="1">
      <template #default>
        <div>
          <DxToolbar id="toolbar">
            <DxItem
              widget="dxButton"
              :options="buttonOptions"
              location="before"
            />
          </DxToolbar>
          <DxDrawer
            :minSize="37"
            :height="900"
            template="list"
            :opened="isDrawerOpen"
          >
            <template #list>
              <!-- <div style="width: 400px" class="simple-treeview-container"> -->
              <DxTreeView
                id="simple-treeview"
                :items="TreeNavItem"
                :width="300"
                :select-by-click="true"
                @itemClick="selectItem"
              />
              <!-- </div> -->
            </template>
            <div id="view">
              <DxSortable
                filter=".dx-tab"
                v-model:data="tabIndexList"
                item-orientation="horizontal"
                drag-direction="horizontal"
                @drag-start="onTabDragStart($event)"
                @reorder="onTabDrop($event)"
              >
                <div>
                  <DxTabPanel
                    v-model:dataSource="tabIndexList"
                    height="800px"
                    :defer-rendering="false"
                    :show-nav-buttons="true"
                    :repaint-changes-only="true"
                    v-model:selected-index="tabselectedIndex"
                    v-model:selectedItem="tabSelectedItem"
                    @titleClick="onTabItemClick"
                    itemTitleTemplate="titleTem"
                    item-template="itemTemplate"
                  >
                    <template #titleTem="{ data: SingletabIndex }">
                      <div>
                        <span>{{ SingletabIndex.title }}</span
                        ><i
                          v-show="showCloseButton()"
                          class="dx-icon dx-icon-close"
                          @click="closeButtonHandler(SingletabIndex)"
                        />
                      </div>
                    </template>
                    <template #itemTemplate="{ data: SingletabIndex }">
                      <div>
                        {{ SingletabIndex.text }}
                        <router-view></router-view>
                        <!-- <PSImainListView /> -->
                        <!-- <keep-alive>
                          <component :is="currentTabComponent"></component>
                        </keep-alive> -->
                      </div>
                    </template>
                  </DxTabPanel>
                </div>
              </DxSortable>
            </div>
          </DxDrawer>
        </div>
      </template>
    </DxItem>
  </DxBox>
</template>

 <script>
import PSIwarehousingMainView from "./PSIcheckoutMainView.vue";
import { DxBox, DxItem } from "devextreme-vue/box";
import DxDrawer from "devextreme-vue/drawer";
import DxSortable from "devextreme-vue/sortable";
import DxTreeView from "devextreme-vue/tree-view";
import DxTabPanel from "devextreme-vue/tab-panel";
import DxToolbar from "devextreme-vue/toolbar";
import PSImainListView from "./PSImainListView.vue";
import { ref, reactive } from "vue";
export default {
  name: "PSImainView",
  components: {
    DxBox,
    DxItem,
    DxDrawer,
    DxSortable,
    DxToolbar,
    DxTreeView,
    DxTabPanel,
    PSImainListView,
    PSIwarehousingMainView,
  },
  data() {
    return {
      currentTabComponent: "",

      isDrawerOpen: true,
      buttonOptions: {
        icon: "menu",
        onClick: () => {
          this.isDrawerOpen = !this.isDrawerOpen;
        },
      },
      TreeNavItem: [
        {
          id: "1",
          text: "系统菜单",
          expanded: true,
          items: [
            {
              id: "1_1",
              text: "入库管理（入库单列表）",
              expanded: true,
              router: "warehousing",
              items: [
                {
                  id: "1_1_1",
                  text: "采购入库单",
                  router: "warehousingpurchase",
                },
                {
                  id: "1_1_2",
                  text: "生产入库单",
                  router: "warehousingproduct",
                },
                {
                  id: "1_1_3",
                  text: "退料入库单",
                },
                {
                  id: "1_1_4",
                  text: "销售退货单",
                },
                {
                  id: "1_1_5",
                  text: "其他入库单",
                },
              ],
            },
            {
              id: "1_2",
              text: "出库管理（出库单列表）",
              items: [
                {
                  id: "1_2_1",
                  text: "销售出库单",
                },
                {
                  id: "1_2_2",
                  text: "领料出库单",
                },
                {
                  id: "1_2_3",
                  text: "采购出货单",
                },
                {
                  id: "1_2_4",
                  text: "其他出货单",
                },
              ],
            },
            {
              id: "1_3",
              text: "数据库导出备份",
              expanded: true,
              router: "dbexportbackup",
            },
            {
              id: "1_4",
              text: "SQL文档",
              expanded: true,
              router: "sqldocument",
              items: [
                {
                  id: "1_4_1",
                  text: "人事SQL文档",
                  router: "sqldocument/renshi",
                },
                {
                  id: "1_4_2",
                  text: "销售SQL文档",
                  router: "sqldocument/xiaoshou",
                },
                {
                  id: "1_4_3",
                  text: "考勤SQL文档",
                  router: "sqldocument/kaoqing",
                },
              ],
            },
          ],
        },
      ],
      tabIndexList: [
        {
          title: "主页",
          router: "homepage",
        },
        // {
        //   title: "入库管理",
        //   router: "warehousing",
        // },
        // {
        //   title: "出库管理",
        //   router: "",
        // },
        // {
        //   title: "SQL文档",
        //   router: "sqldocument",
        // },
      ],

      tabSelectedItem: {},
      tabselectedIndex: 0,
    };
  },
  setup() {
    const tabIndexList2 = reactive([
      {
        title: "主页2",
        text: "John Smith, 1986",
      },
      {
        title: "入库管理2",
        text: "phone: (555)555-5555, email: John.Smith@example.com",
      },
      {
        title: "出库管理2",
        text: "CA San Francisco Stanford Ave st.",
      },
      {
        title: "原始项目2",
        text: "CA San Francisco Stanford Ave st.",
      },
    ]);
    const selectedIndex2 = ref(0);
    return {
      tabIndexList2,
      selectedIndex2,
    };
  },
  mounted() {
    // this.$router.replace({ path: "mainlist" });
  },
  methods: {
    onTabItemClick(e) {
      console.log(e);
      this.$router.replace({ path: `${e.itemData.router}` });
    },
    closeButtonHandler(SingletabIndex) {
      let closeTabIndex = this.tabIndexList.indexOf(SingletabIndex);
      console.log("closetabindex", closeTabIndex);

      this.tabIndexList = this.tabIndexList.filter(
        (item) => item != SingletabIndex
      );
      console.log(
        "closetabindex2",
        closeTabIndex,
        "tabIndexList.length",
        this.tabIndexList.length
      );

      if (closeTabIndex == this.tabIndexList.length) {
        this.tabselectedIndex = this.tabIndexList.length - 1;
        console.log("enter");
      }
      this.$router.replace({ path: "/homepage" });
      console.log(this.tabselectedIndex);
    },

    selectItem(e) {
      console.log("点击了树状导航的", e);
      //   this.tabIndexList.push({ title: "测试", text: "测试内容" });

      // this.tabIndexList2=this.tabIndexList2.concat({ title: "测试", text: "测试内容" });
      this.tabIndexList = [
        ...this.tabIndexList,
        { title: e.itemData.text, router: e.itemData.router },
      ];
      this.tabselectedIndex = this.tabIndexList.length - 1;
      this.$router.push(`${"/" + e.itemData.router}`);
      // this.$router.replace({ path: "sqldocument/kaoqing" });
      console.log(this.tabIndexList, "selectIndex", this.tabselectedIndex);
    },
    showCloseButton() {
      return this.tabIndexList.length > 1;
    },
    onTabDragStart(e) {},
    onTabDrop(e) {},
  },
};
</script>
              
<style>
#simple-treeview {
  background-color: darkgrey;
}
#view-container {
  overflow-y: scroll;
}
</style>
            