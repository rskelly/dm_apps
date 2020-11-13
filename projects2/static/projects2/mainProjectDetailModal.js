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
      dates: [],
      dates_loading: false,
      new_ot_desc: null,

      //cal field but for some reason cannot use computed fields
      totalOTHours: 0,
      totalOTCalcHours: 0,
      totalOTDescription: "",
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
    toggleOTCalc() {
      this.showOTCalc = !this.showOTCalc;
      // if the modal is open, let's fetch the dates
      if (this.showOTCalc) this.getDates(this.year.fiscal_year);
    },
    getDates(fiscalYearId) {
      this.dates_loading = true;
      let endpoint = `/api/project-planning/get-dates/?year=${fiscalYearId}`;
      apiService(endpoint)
          .then(response => {
            this.dates_loading = false;
            this.dates = response;
          })
    },
    processOT() {
      userInput = confirm(processOTMsg)
      if (userInput) {
        this.staff.overtime_hours = this.totalOTCalcHours;
        this.staff.overtime_description = this.totalOTDescription.replaceAll("<br>", "\n");
        this.toggleOTCalc()
      }
    },
    updateDate(date) {
      // we need 2 things: calculated OT and description of OT
      if (date.is_stat || date.int_weekdy === "0") {
        date.calc_ot = date.ot_hours * 2
        date.ot_description = `${date.short_weekday} ${date.formatted_short_date}: ${date.ot_hours}h x 2 = ${date.calc_ot}h`
        if (date.is_stat) date.ot_description += " (stat.)<br>"
        else date.ot_description += "<br>"
      } else {
        // a little more complicated
        if (date.int_weekday === "6" && Number(date.ot_hours) > 7.5) {
          diff = date.ot_hours - 7.5
          date.calc_ot = (7.5 * 1.5) + diff * 2
          date.ot_description = `${date.short_weekday} ${date.formatted_short_date}: 7.5h x 1.5 = 11.25h<br>`
          date.ot_description += `${date.short_weekday} ${date.formatted_short_date}: ${diff}h x 2 = ${Number(diff) * 2}h<br>`
        } else {
          date.calc_ot = date.ot_hours * 1.5
          date.ot_description = `${date.short_weekday} ${date.formatted_short_date}: ${date.ot_hours}h x 1.5 = ${date.calc_ot}h<br>`
        }
      }

      // total OT hours
      this.totalOTHours = 0;
      this.totalOTCalcHours = 0;
      this.totalOTDescription = "";
      for (var i = 0; i < this.dates.length; i++) {
        var d = this.dates[i];
        if (d.ot_hours) this.totalOTHours += Number(d.ot_hours)
        if (d.calc_ot) this.totalOTCalcHours += Number(d.calc_ot)
        if (d.ot_description) this.totalOTDescription += d.ot_description
      }
    },
  },
  computed: {
    // totalOTHours() {
    //   var total = 0;
    //   for (var i = 0; i < this.dates.length; i++) {
    //     var d = this.dates[i];
    //     if (d.ot_hours) total += Number(d.ot_hours)
    //   }
    //   return total
    // },
    // totalOTCalcHours() {
    //   var total = 0;
    //   for (var i = 0; i < this.dates.length; i++) {
    //     var d = this.dates[i];
    //     if (d.calc_ot) total += Number(d.calc_ot)
    //   }
    //   return total
    // },
    // totalOTDescription() {
    //   var myStr = "";
    //   for (var i = 0; i < this.dates.length; i++) {
    //     var d = this.dates[i];
    //     if (d.ot_description) myStr += d.ot_description
    //   }
    //   return myStr
    // },
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