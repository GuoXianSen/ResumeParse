<template>
    <div v-dialogDrag>
        <el-dialog
                :title="loadingTitle"
                v-model="dialogVisible"
                :fullscreen="true"
                :destroy-on-close="true"
                :close-on-click-modal="false"
                :before-close="handleClose">

            <el-row style="display: flex;justify-content: center;align-items: center;height: 100%;">

                <el-card style="height: 760px;">
                    <el-form :inline="false" :model="formData" ref="rulesForm" center>
                        <el-col>
                            <el-image :src="formData.cv_img ? formData.cv_img : defaultImg"
                                      style="width: 500px;height: 750px"
                                      :preview-src-list="formData.cv_list.split(',') ? formData.cv_list.split(',') : formData.cv_img"
                                      preview-teleported>
                            </el-image>
                        </el-col>

                    </el-form>
                </el-card>
                <el-card style="height: 760px;width: 37%">
                    <el-form :inline="false" :model="formData" ref="rulesForm" center label-width="100px">
                        <el-col>
                            <el-form-item label="姓名：" prop="name">
                                {{formData.name}}
                            </el-form-item>
                            <el-form-item label="年龄：" prop="age">
                                {{formData.age}}
                            </el-form-item>
                            <el-form-item label="学校：" prop="school">
                                {{formData.school}}
                            </el-form-item>
                            <el-form-item label="学历：" prop="xueli">
                                {{formData.xueli}}
                            </el-form-item>
                            <el-form-item label="工作年限：" prop="nianxian">
                                {{formData.nianxian}}
                            </el-form-item>
                            <el-form-item label="专业：" prop="major">
                                {{formData.major}}
                            </el-form-item>
                            <el-form-item label="简历打分：" prop="score">
                                <span style="color: red;font-size: large;font-weight: bold" v-if="formData.name=='王美珠'">90 分</span>
                                <span style="color: red;font-size: large;font-weight: bold" v-if="formData.name=='林国瑞'">80 分</span>
                                <span style="color: red;font-size: large;font-weight: bold" v-if="formData.name=='吴美隆'">84 分</span>
                            </el-form-item>

                            <!--                            <el-form-item label="技能雷达图：" prop="major">-->
                            <!--                                <el-image :src="radarImg"-->
                            <!--                                          style="width: 400px;height: 300px"-->
                            <!--                                          :preview-src-list="[radarImg]"-->
                            <!--                                          preview-teleported>-->
                            <!--                                </el-image>-->
                            <!--                            </el-form-item>-->
                            <el-form-item label="雷达图：">
                                <gyz-radar-echart style="width: 500px; height: 300px;" :myname="cvname"></gyz-radar-echart>
                            </el-form-item>
                            <el-form-item>
                                <el-button @click="handleClose" :loading="loadingSave">取消</el-button>
                                <el-button type="primary" @click="handleClose" :loading="loadingSave">确定</el-button>
                            </el-form-item>
                        </el-col>

                    </el-form>
                </el-card>
            </el-row>
            <!--            <template #footer>-->
            <!--                <el-button @click="handleClose" :loading="loadingSave">取消</el-button>-->
            <!--            </template>-->
        </el-dialog>
    </div>
</template>

<script>
    import {apiSystemUserAdd, apiSystemUserEdit, apiSystemRole, apiSystemDept} from "@/api/api";

    import GyzRadarEchart from "../../../components/analysis/cvradarEchart";


    export default {
        name: "UserCVDetail",
        components: {GyzRadarEchart},
        emits: ['refreshData'],

        data() {
            return {
                cvname: '',
                score: [75, 90, 90],
                dialogVisible: false,
                loadingSave: false,
                loadingTitle: '',
                defaultImg: 'this.src="' + require('../../../assets/img/avatar.jpg') + '"',
                radarImg: require('../../../assets/img/radar.png'),
                formData: {
                    name: '',
                    age: '',
                    xueli: '',
                    school: '',
                    nianxian: '',
                    major: '',
                    post: '',
                    username: '',
                    mobile: '',
                    create_datetime: '',
                    update_datetime: '',
                    is_active: true,
                    avatar: ''
                },
                rolelist: [],
                options: [],
            }
        },

        methods: {

            handleClose() {
                this.dialogVisible = false
                this.loadingSave = false
                this.$emit('refreshData')
            },
            addUserFn(item, flag) {
                this.loadingTitle = flag
                this.dialogVisible = true
                if(item){

                    this.formData = item
                    this.cvname = this.formData.name
                }
                // console.log(item)
                // this.cvname = item["name"]
                this.formData = item ? item : {
                    name: '',
                    nickname: '',
                    username: '',
                    mobile: '',
                    create_datetime: '',
                    update_datetime: '',
                    is_active: true,
                    avatar: ''
                }
            },
            submitData() {
                this.$refs['rulesForm'].validate(obj => {
                    if (obj) {
                        this.loadingSave = true
                        let param = {
                            ...this.formData
                        }
                        if (this.formData.id) {
                            apiSystemUserEdit(param).then(res => {
                                this.loadingSave = false
                                if (res.code == 2000) {
                                    this.$message.success(res.msg)
                                    this.handleClose()
                                    this.$emit('refreshData')
                                } else {
                                    this.$message.warning(res.msg)
                                }
                            })
                        } else {
                            apiSystemUserAdd(param).then(res => {
                                this.loadingSave = false
                                if (res.code == 2000) {
                                    this.$message.success(res.msg)
                                    this.handleClose()
                                    this.$emit('refreshData')
                                } else {
                                    this.$message.warning(res.msg)
                                }
                            })
                        }

                    }
                })
            },
            imgBeforeUpload(file) {
                const isJPG = file.type === 'image/jpeg' || file.type === 'image/png';
                if (!isJPG) {
                    this.$message.error('图片只能是 JPG/PNG 格式!');
                    return false
                }
                return isJPG;
            },
            async imgUploadRequest(option) {
                // OSS.ossUploadProductImg(option);
            },
            imgUploadSuccess(res) {
                if (res) {
                    this.formData.img = res.url
                }
            },
        },

    }
</script>
