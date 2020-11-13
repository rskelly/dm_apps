Vue.component("modal", {
  template: "#modal-template",
  delimiters: ["${", "}"],
  props: {
    type: {
      type: String,
      required: true,
    },
    year: {
      type: Object,
      required: true,
    },
    mystaff: {
      type: Object,
      required: false,
    }
  },
  data() {
    return {
      staff: {
        name: null,
        user: null,
        funding_source: null,
        is_lead: null,
        employee_type: null,
        level: null,
        duration_weeks: null,
        overtime_hours: null,
        overtime_description: null,
        student_program: null,
        amount: 0,
      },
      errors: null,
      disableNameField: false,
      disableStudentProgramField: false,
      disableAmountField: false,
      disableLevelField: false,
      projectLeadWarningIssued: false,

      showOTCalc: false,
    }
  },
  methods: {
    onSubmit() {
      this.errors = null
      if (this.type === "staff") {
        if (this.mystaff) {
          let endpoint = `/api/project-planning/staff/${this.mystaff.id}/`;
          apiService(endpoint, "PATCH", this.staff).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        } else {
          let endpoint = `/api/project-planning/project-years/${this.year.id}/staff/`;
          apiService(endpoint, "POST", this.staff).then(response => {
            if (response.id) this.$emit('close')
            else {
              var myString = "";
              for (var i = 0; i < Object.keys(response).length; i++) {
                key = Object.keys(response)[i]
                myString += String(key) + ": " + response[key] + "<br>"
              }
              this.errors = myString
            }
          })
        }
      }

      // regardless of what happens, emit a `close` signal
      // this.$emit('close')

    },
    adjustStaffFields() {

      // if not a student, disable the student program field
      if (this.staff.employee_type !== "4") {
        this.staff.student_program = null;
        this.disableStudentProgramField = true;
      } else {
        this.disableStudentProgramField = false;
      }

      // if employee type is fte, disable "cost" field and the "level" field.
      // do the same If they are a seasonal indeterminate  paid from a-base
      if (this.staff.employee_type === "1" || (this.staff.employee_type === "6" && this.staff.funding_source === "1")) {
        this.staff.amount = null;
        this.disableAmountField = true;
        this.staff.level = null;
        this.disableLevelField = true;
      } else {
        this.disableAmountField = false;
        this.disableLevelField = false;
      }


      // if there is a DFO user, disable the text name field
      if (this.staff.user) {
        this.staff.name = null;
        this.disableNameField = true;
      } else {
        this.disableNameField = false;
      }
      // if the current user is changing themselves away from project lead, give them a warning
      if (currentUser === this.staff.user && !this.staff.is_lead && !this.projectLeadWarningIssued) alert(warningMsg);

    },
    toggleOTCalc () {
      this.showOTCalc = ! this.showOTCalc;
    }
  },
  created() {
    this.$nextTick(() => {
      if (this.mystaff && this.mystaff.id) {
        this.staff = this.mystaff
        // there is an annoying thing that has to happen to convert the html to js to pytonese...
        if (this.staff.is_lead) this.staff.is_lead = "True"
        else this.staff.is_lead = "False"
      }
      this.adjustStaffFields()
    })

  },
  mounted() {


  }
});