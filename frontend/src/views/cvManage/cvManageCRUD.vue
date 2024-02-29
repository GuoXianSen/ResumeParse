<template>
    <div>
        <ly-crud ref="lycrud"  v-bind="crudConfig" >
            <template v-slot:customHandle="slotProps">
                <span class="table-operate-btn" @click="handleClick(slotProps.row,'disable')" v-show="hasPermission('cvManageCRUD','Disable')">禁用</span>
            </template>
        </ly-crud>
    </div>
</template>

<script lang="jsx">
    import {CvsCvs,CvsCvsAdd,CvsCvsDelete,CvsCvsEdit,CvsCvsdisableEdit,CvsCvsExportexecl} from '@/api/api'
    import LyCrud from "@/components/lycrud";
    import templateData from "@/components/dict/crudTemplateData"
    import { h,resolveComponent } from 'vue';
    export default {
        name: "cvManageCRUD",
        components: {LyCrud},
        data(){
            return{
                defaultImg:require('../../assets/img/avatar.jpg'),
                //crud配置
                crudConfig:{
                    //crud请求方法配置
                    crudRequest:{
                        add:CvsCvsAdd,
                        del:CvsCvsDelete,
                        edit:CvsCvsEdit,
                        search:CvsCvs,
                    },
                    //搜索栏目配置
                    searchBar:{
                        showSearchBar:true,//显示搜索栏目
                        searchColums:[
                            {label:'用户名',type:'input',prop:'username',width:200,maxlength:60,placeholder:'请输入用户名'},
                            {label:'手机号',type:'input',prop:'mobile',width:200,maxlength:60,placeholder:'请输入手机号'},
                            {label:'状态',type:'select',prop:'is_active',width:100,placeholder:'请选择',
                                options:[
                                    {value:1,label:'正常'},
                                    {value:0,label:'禁用'}
                                ]
                            },
                            {label:'创建时间',type:'datepicker-datetimerange',prop:'timers'},
                        ]
                    },
                    //显示分页
                    showPagination:true,
                    //分页配置
                    pageparams: {
                        limit: 10,//每页显示的条数(默认每页显示10条)//非必填
                        //pageSizes:[10,20,30,40,50,200],//非必填
                        // layout:'total, sizes, prev, pager, next, jumper',//非必填
                    },
                    //crud按钮配置
                    rowHandle:{
                        width: 180,//操作列宽度
                        fixed:"right",//固定操作列在右侧
                        permission:{//增删改查按钮权限控制（是否显示）
                            add:this.hasPermission('cvManageCRUD','Create'),//bool型
                            del:this.hasPermission('cvManageCRUD','Delete'),
                            edit:this.hasPermission('cvManageCRUD','Update'),
                            search:this.hasPermission('cvManageCRUD','Search'),
                            detail:this.hasPermission('cvManageCRUD','Retrieve'),
                        }
                    },
                    //crud弹窗属性
                    formOptions: {
                        width:'45%',//dialog弹窗宽度：类型：百分比或字符串
                        gutter: 20, // Layout布局栅格间隔
                    },
                    //crud表格属性
                    tableOptions:{
                        border:true,
                        showHeader:true,
                    },
                    showSelectable:true,//表格显示复选项框
                    //table表头列
                    tableColumns:[
                         // {label:'用户头像',type:'image',prop:'avatar',minWidth:'60',sortable: false,hidden:false,render:(row)=>{
                         //     let elImage = resolveComponent('el-image')//全局组件需要先resolveComponent解析该组件再render渲染，不然该标签会出现原样输出
                         //     return h(elImage,{
                         //          src:row.avatar ? row.avatar : this.defaultImg,
                         //          previewSrcList:[row.avatar ? row.avatar : this.defaultImg],//开启预览，原preview-src-list属性在h渲染方法中，-后字母大写代替即可：previewSrcList
                         //          previewTeleported:true,//插入至body元素上
                         //          style:"width: 30px;height: 30px",
                         //     },)
                         //  }
                         // },
                        {label:'ID',prop:'id',type:'input',minWidth:'100',sortable: false,hidden:true,
                            form:{
                                 //表单属性
                                 span:24,
                                 hidden:true,//编辑时隐藏，添加时去除
                             }
                        },
                        {label:'用户头像',type:'image-avatar',prop:'avatar',minWidth:'60',sortable: false,hidden:false,
                            render:(row)=>{
                                //jsx语法
                                return <el-image src={row.avatar ? row.avatar : this.defaultImg} style="width: 30px;height: 30px" preview-teleported={true} preview-srcList={[row.avatar ? row.avatar : this.defaultImg]}></el-image>
                            },
                            form:{
                                //表单属性
                                span:24,
                                // width:80,头像大小默认80px
                            }

                         },
                         {label:'姓名',prop:'name',type:'input',minWidth:'110',sortable: false,hidden:false,
                            form:{
                                //表单属性
                                span:12,
                                rules: [{ required: true, message: '姓名必填项' }],
                                placeholder: '请输入姓名',
                            }
                         },
                         {label:'年龄',prop:'age',type:'input',minWidth:'50',sortable: false,hidden:false,
                            form:{
                                //表单属性
                                span:12,
                                rules: [{ required: true, message: '年龄必填项' }],
                                placeholder: '请输入年龄',
                            }
                         },
                         {label:'毕业院校',prop:'school',type:'input',minWidth:'100',sortable: false,hidden:false,
                            form:{
                                //表单属性
                                span:12,
                                rules: [{ required: true, message: '毕业院校必填项' }],
                                placeholder: '请输入毕业院校',
                            }
                         },
                         {label:'专业',prop:'major',type:'input',minWidth:'100',sortable: false,hidden:false,
                            form:{
                                //表单属性
                                span:12,
                                rules: [{ required: true, message: '专业必填项' }],
                                placeholder: '请输入专业',
                            }
                         },
                         {label:'工作年限',prop:'nianxian',type:'input',minWidth:'60',sortable: false,hidden:false,
                            form:{
                                //表单属性
                                span:12,
                                rules: [{ required: true, message: '工作年限必填项' }],
                                placeholder: '请输入工作年限',
                            }
                         },
                         {label:'学历',prop:'xueli',type:'input',minWidth:'100',sortable: false,hidden:false,
                            form:{
                                //表单属性
                                span:12,
                                rules: [{ required: true, message: '学历必填项' }],
                                placeholder: '请输入学历',
                            }
                         },
                    ],
                },

            }
        },
        methods:{
            //自定义操作列按钮方法
            handleClick(row,flag){
                let vm = this
                if(flag=='disable'){
                    UsersUsersdisableEdit({id:row.id}).then(res=>{
                        if(res.code == 2000) {
                            vm.$message.success(res.msg)
                            vm.$refs.lycrud.handleRefresh()//刷新表格数据
                        } else {
                            vm.$message.warning(res.msg)
                        }
                    })
                }
            },
        },
    }
</script>

<style scoped>

</style>
