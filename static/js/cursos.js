let formdata = new FormData();
formdata.append("wstoken", "2fb3df9ba2006ef257f072651b547b3d");
formdata.append("moodlewsrestformat", "json");
formdata.append("wsfunction", "core_course_get_courses");

let reqOptions = {
url: "http://academyec.com/moodle/webservice/rest/server.php",
method: "POST",
data: formdata,
}


new Vue({
    el: '#lista_courses',
    delimiters: ['{$', '$}'],
    data () {
        return {
            courses: null,
            content_course: null,
            content_courseByModule: null, 
        }
    },
    mounted (){
        this.getCourses()
    },
    methods:{
        getCourses(){
            axios.request(reqOptions)
            .then(response => {
                this.courses = response.data
                })
        },
        getDetailCourse(id){
            let formdataC = new FormData();
            formdataC.append("wstoken", "2fb3df9ba2006ef257f072651b547b3d");
            formdataC.append("moodlewsrestformat", "json");
            formdataC.append("wsfunction", "core_course_get_contents");
            formdataC.append("courseid", id);

            let reqOptionsC = {
                url: "http://academyec.com/moodle/webservice/rest/server.php",
                method: "POST",
                data: formdataC,
            }

            axios.request(reqOptionsC)
            .then(response => {
                this.content_course = response.data;
                })
        },
        getContentCourseByModule(id){
            for (const i of this.content_course) {
                if (i.id == id) {
                    this.content_courseByModule = i.modules
                }
            }
        }
    }
});