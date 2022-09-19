let TOKEN_MOODLE = '2fb3df9ba2006ef257f072651b547b3d'

let formdata = new FormData();
formdata.append("wstoken", TOKEN_MOODLE);
formdata.append("moodlewsrestformat", "json");
formdata.append("wsfunction", "core_course_get_course_content_items");
formdata.append("courseid", "1");

let formdataCourse = new FormData();
formdataCourse.append("wstoken", TOKEN_MOODLE);
formdataCourse.append("moodlewsrestformat", "json");
formdataCourse.append("wsfunction", "core_course_get_courses");

new Vue({
    el: '#fomCalendario',
    delimiters: ['{$', '$}'],
    data () {
        return {
            item: null,
            curso: null,
            name: null,
            description: null,
            format: 1,
            courseid: null,
            groupid: 0,
            repeats: 0,
            eventtype: null,
            timestart: null,
            timeend: null,
            visible: 1,
            sequence: 1,
        }
    },
    mounted () {
        this.getItemList();
        this.getCourseList();
    },
    methods:{
        getCourseList(){
            let reqOptions = {
                url: "http://academyec.com/moodle/webservice/rest/server.php",
                method: "POST",
                data: formdataCourse,
            }
            axios.request(reqOptions)
           .then(response => {
               this.curso = response.data;
           })
              .catch(error => {
                console.log(error);
            })
        },
        getItemList(){
            let reqOptions = {
                url: "http://academyec.com/moodle/webservice/rest/server.php",
                method: "POST",
                data: formdata,
            }
            axios.request(reqOptions)
           .then(response => {
               this.item = response.data.content_items;
           })
              .catch(error => {
                console.log(error);
            })
        },
        getInputCalendar(){
            let ttiTimeStart = parseInt(((new Date(this.timestart).getTime() / 1000) + 86400).toFixed(0))
            let ttiTimeEnd = parseInt(((new Date(this.timeend).getTime() / 1000) + 86400).toFixed(0))
            let ttiDuration = ttiTimeEnd - ttiTimeStart;

            let formdata = new FormData();
            formdata.append("wstoken", "2fb3df9ba2006ef257f072651b547b3d");
            formdata.append("moodlewsrestformat", "json");
            formdata.append("wsfunction", "core_calendar_create_calendar_events");
            formdata.append("events[0][name]", this.name);
            formdata.append("events[0][description]", this.description);
            formdata.append("events[0][format]", "1");
            formdata.append("events[0][courseid]", this.courseid);
            formdata.append("events[0][groupid]", "0");
            formdata.append("events[0][repeats]", "0");
            formdata.append("events[0][eventtype]", this.eventtype);
            formdata.append("events[0][timestart]", ttiTimeStart);
            formdata.append("events[0][timeduration]", ttiDuration);
            formdata.append("events[0][visible]", "1");
            formdata.append("events[0][visible]", "1");

            let bodyContent =  formdata;

            let reqOptions = {
            url: "http://academyec.com/moodle/webservice/rest/server.php",
            method: "POST",
            data: bodyContent,
            }
            
            if(this.name == null || this.description == null || this.courseid == null || this.eventtype == null || this.timestart == null || this.timeend == null){
                alert("Por favor, complete todos los campos");
            } else {
                axios.request(reqOptions)
                .then(function (response) {
                    alert('Evento creado exitosamente')
                    location.reload()
                    })
                .catch(function (error) {
                    console.log(error);
                });
            }
            
        }
    }
});
