<template>
    <div>

        <ly-dialog v-model="dialogVisible" :title="loadingTitle" width="560px" :before-close="handleClose">
            <el-row style="display: flex;justify-content: center;align-items: center;height: 100%;">
                <el-card style="height: 760px;">
                    <el-col>
                        <el-image :src="formData.cv_img ? formData.cv_img : defaultImg"
                                  style="width: 500px;height: 750px"
                                  :preview-src-list="formData.cv_list.split(',') ? formData.cv_list.split(',') : formData.cv_img"
                                  preview-teleported>
                        </el-image>
                    </el-col>
                </el-card>

                <el-card  style="height: 760px;">
                    <br><br><br><br><br><br><br><br><br>
                    <el-col>
                        <el-form :inline="false" :model="formData" :rules="rules" ref="rulesForm" position="left"
                                 label-width="100px">
                            <el-form-item label="上传简历：">

                                <el-upload
                                        ref="uploadRef"
                                        class="upload-demo"
                                        :http-request="imgUploadRequest"
                                        :before-upload="fileBeforeUpload">


                                    <template #trigger>
                                        <el-button
                                                type="primary">上传简历
                                        </el-button>
                                    </template>

                                    &nbsp;
                                    <el-button class="ml-3" type="success" @click="fileUploadRequest">
                                        解析简历
                                    </el-button>

                                    <template #tip>
                                        <div class="el-upload__tip">
                                            支持DOC、DOCX、JPEG、PNG、PDF等多种格式。
                                        </div>
                                    </template>
                                </el-upload>
                            </el-form-item>

                            <el-form-item label="姓名：" prop="name">
                                <el-input v-model="formData.name"></el-input>
                            </el-form-item>
                            <el-form-item label="年龄：" prop="age">
                                <el-input v-model="formData.age"></el-input>
                            </el-form-item>
                            <el-form-item label="毕业院校：" prop="school">
                                <el-input v-model="formData.school"></el-input>
                            </el-form-item>
                            <el-form-item label="工作年限：" prop="nianxian">
                                <el-input v-model="formData.nianxian"></el-input>
                            </el-form-item>
                            <el-form-item label="专业：" prop="major">
                                <el-input v-model="formData.major"></el-input>
                            </el-form-item>
                            <el-form-item label="学历：" prop="xueli">
                                <el-select v-model="formData.xueli" clearable placeholder="请在选项菜单中选择学历">
                                    <el-option
                                            v-for="item in options"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value"
                                    />
                                </el-select>
                                <!--                    <el-input v-model="formData.xueli"></el-input>-->
                            </el-form-item>
                            <!--                <el-form-item label="状态：" prop="is_active">-->
                            <!--                    <el-switch-->
                            <!--                        v-model="formData.is_active"-->
                            <!--                        active-color="#13ce66"-->
                            <!--                        inactive-color="#ff4949">-->
                            <!--                    </el-switch>-->
                            <!--                </el-form-item>-->
                            <el-form-item>
                                <el-button @click="handleClose" :loading="loadingSave">取消</el-button>
                                <el-button type="primary" @click="submitData" :loading="loadingSave">确定</el-button>
                            </el-form-item>
                        </el-form>


                    </el-col>
                </el-card>
            </el-row>
            <!--                    <template #footer>-->
            <!--                        <el-button @click="handleClose" :loading="loadingSave">取消</el-button>-->
            <!--                        <el-button type="primary" @click="submitData" :loading="loadingSave">确定</el-button>-->
            <!--                    </template>-->

        </ly-dialog>
    </div>
</template>


<script>
    import {
        CvUploadAdd,
        CvUploadEdit,
        platformsettingsUploadPlatformImg,
        platformsettingsUploadPlatformFile
    } from "@/api/api";
    import LyDialog from "../../../components/dialog/dialog";
    import {ref} from "vue";
    import {ElMessage} from 'element-plus'

    export default {
        name: "addUserCV",
        components: {LyDialog},
        emits: ['refreshData'],
        data() {
            return {
                myobj: null,
                srcList: [],
                dialogVisible: false,
                loadingSave: false,
                loadingTitle: '',
                defaultImg: require('../../../assets/img/default.png'),
                formData: {
                    name: '',
                    age: '',
                    school: '',
                    xueli: '',
                    major: '',
                    nianxian: '',
                    cv_img: '',
                    cv_list: ''
                },
                rules: {
                    username: [
                        {required: true, message: '请输入用户名', trigger: 'blur'}
                    ],
                    // nickname: [
                    //     {required: true, message: '请输入昵称',trigger: 'blur'}
                    // ],
                    password: [
                        {required: true, message: '请输入密码', trigger: 'blur'}
                    ],
                    mobile: [
                        {required: true, message: '请输入手机号', trigger: 'blur'}
                    ],
                    is_active: [
                        {required: true, message: '请选择是否启用', trigger: 'blur'}
                    ]
                },
                rolelist: [],
                options: [
                    {
                        label: '无',
                        value: '无',
                    },
                    {
                        label: '小学',
                        value: '小学',
                    },
                    {
                        label: '初中',
                        value: '初中',
                    },
                    {
                        label: '高中',
                        value: '高中',
                    },
                    {
                        label: '中专',
                        value: '中专',
                    },
                    {
                        label: '大专',
                        value: '大专',
                    },
                    {
                        label: '本科',
                        value: '本科',
                    },
                    {
                        label: '硕士',
                        value: '硕士',
                    },
                    {
                        label: '博士',
                        value: '博士',
                    },
                ],
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
                if (item) {
                    delete this.rules.password
                    this.formData = item
                } else {
                    this.rules.password = [
                        {required: true, message: '请输入密码', trigger: 'blur'}
                    ]
                    this.formData = {
                        name: '',
                        age: '',
                        school: '',
                        xueli: '',
                        major: '',
                        nianxian: '',
                        cv_img: '',
                        cv_list: ''
                    }
                }
            },
            submitData() {
                this.$refs['rulesForm'].validate(obj => {
                    if (obj) {
                        this.loadingSave = true
                        let param = {
                            ...this.formData
                        }
                        // param.role = param.role?param.role.split(" "):[]
                        if (this.formData.id) {
                            CvUploadEdit(param).then(res => {
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
                            CvUploadAdd(param).then(res => {
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
            fileBeforeUpload(file) {
                const isTrueFile =
                    file.type === "application/pdf" ||
                    file.type === "image/jpeg" ||
                    file.type === "image/png" ||
                    file.type === "application/msword" ||
                    file.type === "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
                if (!isTrueFile) {
                    this.$message.error('上传的文件只能是DOC、DOCX、PDF、JPEG和PNG格式!');
                    return false
                }
                return isTrueFile;
            },
            async imgUploadRequest(param) {
                // 这里的参数是指在进行文件上传的时候将文件作为参数传进来
                var vm = this

                // 先获得 platformsettingsUploadPlatformImg 的结果
                const imgResult = await platformsettingsUploadPlatformImg(param);
                console.log(imgResult)
                const img = imgResult.data.data['cv_img'];
                console.log("=================")
                console.log(img);
                console.log("=================")
                // 支持多页简历 用img_list来保存
                console.log(imgResult.data.data['img_list'])
                vm.formData.cv_img = img
                // if (Array.isArray(img)){
                //     vm.formData.cv_img = img[0]
                // }
                // else{
                //     vm.formData.cv_img = img
                // }
                if (vm.formData.cv_img === img) {
                    ElMessage.success('简历上传成功！'); // 创建 Element Plus 提示框
                }
                this.srcList = imgResult.data.data['img_list']
                // 需要修改的文件夹

                let mypath = imgResult.data.data['path']
                console.log(mypath)
                // 存储所有的简历图片列表
                console.log("第一部分跑完")
                vm.formData.cv_list = imgResult.data.data['img_list'].toString()


                let obj = await platformsettingsUploadPlatformFile(param, mypath)
                console.log("第二部分 OCR+NER已完成！")

                console.log(obj)
                console.log(obj.data)
                console.log(obj.data.data['毕业院校'])
                console.log(obj.data.data['姓名'])

                if (obj.code == 2000) {
                    ElMessage.success('简历解析即将完成！'); // 创建 Element Plus 提示框
                    // vm.myobj.name = obj.data.data['姓名']
                    // vm.myobj.age = obj.data.data['年龄']
                    // vm.myobj.xueli = obj.data.data['学历']
                    // vm.myobj.school = obj.data.data['毕业院校']
                    // vm.myobj.major = obj.data.data['主修专业']
                    // vm.myobj.nianxian = obj.data.data['工作年限']
                    vm.formData.name = obj.data.data['姓名']
                    vm.formData.age = obj.data.data['年龄']
                    vm.formData.xueli = obj.data.data['学历']
                    vm.formData.school = obj.data.data['毕业院校']
                    vm.formData.major = obj.data.data['主修专业']
                    vm.formData.nianxian = obj.data.data['工作年限']

                } else {
                    vm.$message.warning(res.msg)
                }

            },
            async fileUploadRequest(param) {
                var vm = this
                ElMessage.warning('简历开始解析！'); // 创建 Element Plus 提示框
                console.log("简历解析开始！")
                console.log(this.myobj)
                console.log(this.myobj.name)
                while (this.myobj !== null && this.myobj.data !== undefined) {
                    ElMessage.warning('简历解析成功！'); // 创建 Element Plus 提示框
                    // vm.formData.name = this.myobj.name
                    // vm.formData.age = this.myobj.age
                    // vm.formData.xueli = this.myobj.xueli
                    // vm.formData.school = this.myobj.school
                    // vm.formData.major = this.myobj.major
                    // vm.formData.nianxian = this.myobj.nianxian
                }

            },
            imgUploadSuccess() {
                this.$refs.uploadDefaultImage.clearFiles()
            },


        }
    }
</script>
<style scoped>
    .avatar-uploader .el-upload {
        border: 1px dashed #d9d9d9;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .avatar-uploader .el-upload:hover {
        border-color: #409EFF;
    }

    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 128px;
        height: 128px;
        line-height: 128px;
        text-align: center;
    }

    .avatar {
        width: 128px;
        height: 128px;
        display: block;
    }
</style>

