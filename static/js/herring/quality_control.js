function markTest(testId, testPassed) {
  pass = "passed"
  fail = "failed"
  if (testPassed === null) {
    $("#"+testId).text("")
    $("#"+testId).removeClass("good")
    $("#"+testId).removeClass("bad")
    $("#"+testId).removeClass("mild-concern")

  }
  else if (testPassed === true) {
    $("#"+testId).text(pass)
    $("#"+testId).addClass("good")
    $("#"+testId).removeClass("bad")
    $("#"+testId).removeClass("mild-concern")
  }
  else if (testPassed === false) {
    $("#"+testId).text(fail)
    $("#"+testId).addClass("bad")
    $("#"+testId).removeClass("good")
    $("#"+testId).removeClass("mild-concern")
  }
}

function markTestAccepted(testId, testPassed) {
  pass = "yes"
  fail = "no"
  if (testPassed === null) {
    $("#"+testId).val("")
    $("#"+testId).removeClass("good")
    $("#"+testId).removeClass("bad")
    $("#"+testId).removeClass("mild-concern")
    $("#"+testId)[0].style.opacity = 0
  }
  else if (testPassed === true) {
    $("#"+testId).val(pass)
    $("#"+testId).addClass("good")
    $("#"+testId).removeClass("bad")
    $("#"+testId).removeClass("mild-concern")
    $("#"+testId)[0].style.opacity = 100
  }
  else if (testPassed === false) {
    $("#"+testId).val(fail)
    $("#"+testId).addClass("bad")
    $("#"+testId).removeClass("good")
    $("#"+testId).removeClass("mild-concern")
    $("#"+testId)[0].style.opacity = 100
  }
}

var rangeObject = {
      "fish_length":{
        "possible":{
            "min":1,
            "max":600,
            "comments":"range of historical data based on 344097 observations is  17-480mm",
            },
            "probable":{
                "min":150,
                "max":386,
                "comments":"based on 344097 observations of historical data; [mean +- 2 x SD] = [197.5884, 385.8797]; decision was made in meeting with herring group to allow very small measurements THEREFORE the above comment is moot for the lower bound. Arbitrariliy selected 150 mm as lower bound"
            },
        },
        "fish_weight":{
            "possible":{
                "min":1,
                "max":672,
                "comments":"range of historical data based on 317149 observations is  1 g to  672 g",
            },
            "probable":{
                "min":29,
                "max":412,
                "comments":"based on 317149 observations of historical data; [mean +- 2 x SD] = [ 29.63415, 411.96259]",
            },
        },
        "gonad_weight":{
            "possible":{
                "min":0,
                "max":210,
                "comments":"range of historical data based on 280328 observations is  0.1 g to  204.5 g",
            },
            "probable":{
                "min":0,
                "max":89,
                "comments":"based on 280328 observations of historical data; [mean +- 2 x SD] = [-29.63415, 88.16331]",
            },
        },
        "annulus_count":{
            "possible":{
                "min":0,
                "max":20,
                "comments":"range of historical data based on 280328 observations is  0  to  15",
            },
            "probable":{
                "min":1,
                "max":10,
                "comments":" on 22866 observations of historical data; [mean +- 2 x SD] = [0.9677301 9.1288325]",
            },
        },
    }

// initialize  blank qcFeedback object
var qcFeedbackObject = {}


function testImprobableAccepted(objectType) {
  failedTests = []
  blankTests = []

  if (objectType === "lab_sample") {
    // grab all test related to probability
    testList = [204,207,302,305,308]
    targetTest = 208
  }
  if (objectType === "otolith_sample") {
    // grab all test related to probability
    testList = [209,311]
    targetTest = 211
  }

  // first determine if there is an improbable observation, or if blank; also set formatting on the "accepted" column
  for (var i = 0; i < testList.length; i++) {
    if ($("#display_test_"+testList[i]).text() === "failed") {
      failedTests.push(testList[i])
    }
    else if ($("#display_test_"+testList[i]).text() === "") {
      blankTests.push(testList[i])
    }
    // formatting
    if ($("#id_test_"+testList[i]+"_accepted").val() === "no") {
      markTestAccepted("id_test_"+testList[i]+"_accepted", false)
    } else if ($("#id_test_"+testList[i]+"_accepted").val() === "yes") {
      markTestAccepted("id_test_"+testList[i]+"_accepted", true)
      // remove formatting from the test itself
      $("#display_test_"+testList[i]).removeClass("bad")
      $("#display_test_"+testList[i]).addClass("mild-concern")
    }
  }
  // if all tests are blank, this test should be blank too
  if (blankTests.length === testList.length) {
    markTest("display_test_"+targetTest, null)
  }
  // everything has been tested and there are no failed tests
  else if (failedTests.length === 0 && blankTests.length === 0){
    markTest("display_test_"+targetTest, true)
  }
  // there are some passed tests and no failed tests... remain on standby
  else if (failedTests.length === 0){
    markTest("display_test_"+targetTest, null)
  }
  // finally, there are some failed test and we have to make sure they have been accepted
  else {
    var pass = true;
    for (var i = 0; i < failedTests.length; i++) {
      // check to see if accepted

      if ($("#id_test_"+failedTests[i]+"_accepted").val() !== "yes") {
        console.log("break!");
        // if not, then mark test as failed and leave loop
        markTest("display_test_"+targetTest, false)
        pass= false
        break
      }
    }
    if (pass) {
      // if there are still blank tests, remain on standby
      if (blankTests.length > 0) {
        console.log("hello!");
        markTest("display_test_"+targetTest, null)
      // score test as successful
      }else {
        markTest("display_test_"+targetTest, true)
      }
    }
  }
}

function testPossibleRange(objectType) {
  var stop = false
  if (objectType === "lab_sample") {
    testList = [301,304,307]
    targetTest = 203
  }
  else if (objectType === "otolith_sample") {
    testList = [310,]
    targetTest = 210
  }

  // do one loop to ensure values are present
  for (var i = 0; i < testList.length; i++) {
    if ($("#display_test_"+testList[i]).text() === "") {
      markTest("display_test_"+targetTest, null)
      stop = true
      break
    }
  }
    if (stop === false) {
      // do a second loop to assign a value
      for (var i = 0; i < testList.length; i++) {
        if ($("#display_test_"+testList[i]).text() !== "passed") {
          markTest("display_test_"+targetTest, false)
          break
        }
        else {
          markTest("display_test_"+targetTest, true)
        }
      }
    }
  }

function testDataPoints(fieldName) {
  var stop = false
  var fieldVerboseName = fieldName.replace("_"," ")

  if (fieldName === "fish_length") {
    test = [300,301,302]
  }
  else if (fieldName === "fish_weight"){
    test = [303,304,305]
  }
  else if (fieldName === "gonad_weight"){
    test = [306,307,308]
  }
  else if (fieldName === "annulus_count"){
    test = [309,310,311]
  }
  else {
    // bad fieldName
    stop = true
  }

  // provided a good fieldName was provided
  if (stop === false) {
    // field is not empty
    if ( $("#id_"+fieldName)[0].value === "") {
      markTest("display_test_"+test[0], false)
      markTest("display_test_"+test[1], null)
      markTest("display_test_"+test[2], null)
    }
    else {
      // test 1 is passed
      markTest("display_test_"+test[0], true)
      fieldValue = Number($("#id_"+fieldName)[0].value)

      // check possible range
      if (fieldValue < rangeObject[fieldName].possible.min || fieldValue > rangeObject[fieldName].possible.max ) {
        markTest("display_test_"+test[1], false)
        markTest("display_test_"+test[2], null)
      }
      else{
        // test 2 passed
        markTest("display_test_"+test[1], true)

        // check probable range
        if (fieldValue < rangeObject[fieldName].probable.min || fieldValue > rangeObject[fieldName].probable.max ) {
          markTest("display_test_"+test[2], false)
          // is the test already accepted?
          if ($("#id_test_"+test[2]+"_accepted").val()=="yes") {
            // do nothing
          } else {
            markTestAccepted("id_test_"+test[2]+"_accepted", false)
            // send some information
            var min = parseFloat(Math.round(rangeObject[fieldName].probable.min * 100) / 100).toFixed(1)
            var max = parseFloat(Math.round(rangeObject[fieldName].probable.max * 100) / 100).toFixed(1)
            var msg = `${fieldVerboseName} is outside of the probable range. \n\nA value was expected between ${min} and ${max}. \n\nAre you confident in your measurements? \n\n Press [y] for YES or [n] for NO.`
            var msgLite = `Improbable measurement for ${fieldVerboseName}`

            // write to the qcFeedbackObject
            qcFeedbackObject[test[2]] = {}
            qcFeedbackObject[test[2]].msg = msg
            qcFeedbackObject[test[2]].msgLite = msgLite
            qcFeedbackObject[test[2]].testId = test[2]

          }
        }
        else {
          // test 3 passed
          markTest("display_test_"+test[2], true)
          markTestAccepted("id_test_"+test[2]+"_accepted", null)
        }
      }
    }
  }
}

function testQCPassed(objectType) {
  // make sure to run this as last test
  if (objectType === "lab_sample") {
    // grab all test related to fish detail and see if any failed
    testList = [202,203,208]
    targetTest = 201
  }
  else if (objectType === "otolith_sample") {
    // grab all test related to fish detail and see if any failed
    testList = [206,210,211]
    targetTest = 200

  }

  for (var i = 0; i < testList.length; i++) {
    if ($("#display_test_"+testList[i]).text() !== "passed") {
      markTest("display_test_"+targetTest, false)
      break
    }
    else {
      markTest("display_test_"+targetTest, true)
    }
  }
}

function testMandatoryFields(objectType) {
  if (objectType === "port_sample") {
      var targetTest = 230;
      console.log("hello!")
  }
  else if (objectType === "lab_sample") {
    var targetTest = 202
  }
  else if (objectType === "otolith_sample") {
    var targetTest = 206
  }

  // run the loop
  for (var i = 0; i < $(".mandatory").length; i++) {
    // for the port sample, we are looking to read .innerHTML while for lab and otolith form we read .value
    if (objectType === "port_sample") {
        var myTest = ($(".mandatory")[i].innerHTML === "" || $(".mandatory")[i].innerHTML === "None")
    }
    else {
        var myTest = ($(".mandatory")[i].value === "" || $(".mandatory")[i].value === "None")
    }
    if (myTest) {
      markTest("display_test_"+targetTest, false);
      break
    }
    else {
      markTest("display_test_"+targetTest, true);
    }
  }
}

function test205(lengthFrequencySum, totalFishMeasured) {
  if (lengthFrequencySum === totalFishMeasured) {
    markTest("display_test_205", true)

  }
  else {
    markTest("display_test_205", false)
  }
}

function test231(labProcessingComplete) {
  if (labProcessingComplete) {
    markTest("display_test_231", true)
  }
  else {
    markTest("display_test_231", false)
  }

}

function test232(otolithProcessingComplete) {
  if (otolithProcessingComplete) {
    markTest("display_test_232", true)
  }
  else {
    markTest("display_test_232", false)
  }
}


function improbableMeasurementValidation(talkBack = true) {
    // JSON atributes to check
    testList = [302,305,308,204,207,311,209]

    for (var i = 0; i < testList.length; i++) {
      if (jQuery.isEmptyObject(qcFeedbackObject[testList[i]]) === false) {
        // means there is a problem that needs dealing with
        var test = testList[i]
        var msgLite = qcFeedbackObject[test].msgLite
        var msg = qcFeedbackObject[test].msg

        if (talkBack) {
          speak(msgLite);
        }

        // give the machine a bit of time to catch up!
        setTimeout(testFunc,1200);

        // package the remaining code to be called by the setTimeout func
        function testFunc (){
          var userInput;
          while (userInput !== "y" && userInput !== "n") {
            userInput = prompt(msg).toLocaleLowerCase();
          }

          if (userInput === 'n') {
            giveReadyQueue = false
            if (talkBack) {
              speak("redo measurement");
            }
            markTestAccepted("id_test_"+test+"_accepted", false)

          } else {
            // if user is confident, we will mark yes for accepted
            giveReadyQueue = false
            console.log("id_test_"+test+"_accepted");
            markTestAccepted("id_test_"+test+"_accepted", true)
            if (talkBack) {
              audio.play();
            }
            runTests();
          }
        }
        break
      }
    }
  }

function testGlobalRatio(testId) {
  var stop = false
  if (testId === 204) {
    var independentVar = $("#id_fish_length")[0].value
    var dependentVar = $("#id_fish_weight")[0].value
    if (independentVar !== "" && dependentVar !== "") {
      // set the strings to numbers for further processing
      independentVar = Number($("#id_fish_length")[0].value)
      dependentVar = Number($("#id_fish_weight")[0].value)
      var independentName = "fish length"
      var dependentName = "fish weight"
      var min = Math.exp(-12.978 + 3.18 * Math.log(independentVar))
      var max = Math.exp(-12.505 + 3.18 * Math.log(independentVar))
      var msgLite = `Improbable measurement for ${independentName} : ${dependentName} ratio`
      var msg = `The ${independentName} : ${dependentName} ratio is outside of the probable range. \n\nFor the given value of ${independentName}, ${dependentName} most commonly ranges between ${parseFloat(Math.round(min * 100) / 100).toFixed(1)} and ${parseFloat(Math.round(max * 100) / 100).toFixed(1)}. \n\nAre you confident in your measurements? \n\nPress [y] for YES or [n] for NO.`

    }
    else {
      stop = true
    }
  }
  else if (testId === 207) {
    var independentVar = $("#id_fish_weight")[0].value
    var dependentVar = $("#id_gonad_weight")[0].value
    var factor = Number($("#id_maturity")[0].value)
    // only do the test if all vars are present

    if (independentVar !== "" && dependentVar !== "" && factor !== "") {
      // set the strings to numbers for further processing
      independentVar = Number($("#id_fish_weight")[0].value)
      dependentVar = Number($("#id_gonad_weight")[0].value)

      var independentName = "somatic weight"
      var dependentName = "gonad weight"
      if (factor === 1){
        min = 0
        max = 1
      }
      else if (factor === 2){
        min = 0
        max = Math.exp(-4.13529659279963 + Math.log(independentVar) * 0.901314871086489)
      }
      else if (factor === 3){
        min = Math.exp(-9.73232467962432 + Math.log(independentVar) * 1.89741087890489)
        max = Math.exp(-7.36823392683834 + Math.log(independentVar) * 1.89014326451594)
      }
      else if (factor === 4){
        min = Math.exp(-3.47650267387848 + Math.log(independentVar) * 1.032305979081)
        max = Math.exp(-1.26270682092335 + Math.log(independentVar) * 1.01753432622181)
      }
      else if (factor === 5){
        min = Math.exp(-5.20139782140475 + Math.log(independentVar) * 1.57823918381865)
        max = Math.exp(-4.17515855708087 + Math.log(independentVar) * 1.56631264086027)
      }
      else if (factor === 6){
        min = Math.exp(-4.98077570284809 + Math.log(independentVar) * 1.53819945023286)
        max = Math.exp(-3.99324471338789 + Math.log(independentVar) * 1.53661353195509)
      }
      else if (factor === 7){
        min = Math.exp(-5.89580204167729 + Math.log(independentVar) * 1.27478993476955)
        max = Math.exp(-2.94435270310896 + Math.log(independentVar) * 1.19636077686861)
      }
      else if (factor === 8){
        min = Math.exp(-7.18685438956137 + Math.log(independentVar) * 1.40456267851141)
        max = Math.exp(-5.52714180205898 + Math.log(independentVar) * 1.39515770753421)
      }

      var msgLite = `Improbable measurement for ${independentName} : ${dependentName} ratio`
      var msg = `The ${independentName} : ${dependentName} ratio is outside of the probable range. \n\nFor the given value of ${independentName} at maturity level ${factor}, ${dependentName} most commonly ranges between ${parseFloat(Math.round(min * 100) / 100).toFixed(1)} and ${parseFloat(Math.round(max * 100) / 100).toFixed(1)}. \n\nAre you confident in your measurements? \n\nPress [y] for YES or [n] for NO.`
    }
    else {
      stop = true
    }
  }
  else if (testId === 209) {
    var independentVar = $("#id_fish_length")[0].value
    var dependentVar = $("#id_annulus_count")[0].value
    if (independentVar !=="" && dependentVar !== "") {
      // set the strings to numbers for further processing
      var independentVar = Number($("#id_fish_length")[0].value)
      var dependentVar = Number($("#id_annulus_count")[0].value)
      var independentName = "fish length"
      var dependentName = "annulus count"
      var min = (-14.3554448587879 + 6.34008000506408E-02 * independentVar)
      var max = (-10.1477660949041 + 6.33784283545123E-02 * independentVar)

      var msgLite = `Improbable measurement for ${independentName} : ${dependentName} ratio`
      var msg = `The ${independentName} : ${dependentName} ratio is outside of the probable range. \n\nFor the given value of ${independentName}, ${dependentName} most commonly ranges between ${parseFloat(Math.round(min * 100) / 100).toFixed(1)} and ${parseFloat(Math.round(max * 100) / 100).toFixed(1)}. \n\nAre you confident in your measurements? \n\nPress [y] for YES or [n] for NO.`
    }
    else {
      stop = true
    }
  }
  else {
    stop = true
  }

  // if the test was stopped, it means we are not ready to evaluate and the test should be left blank
  if (stop) {
    markTest("display_test_"+testId, null)
    markTestAccepted("id_test_"+testId+"_accepted", null)
  }
  else {
    console.log(`independent=${independentVar};dependent=${dependentVar};min=${min}; max=${max}`);
    if (dependentVar < min || dependentVar > max){
      markTest("display_test_"+testId, false)

      // check to see if the failed test has already been accepted
      if ($("#id_test_"+testId+"_accepted").val() === "yes") {
        // do nothing
      }
      // if it hasn't, this information should be logged in the qcFeedbackObject
      else {
        // write to the qcFeedbackObject
        qcFeedbackObject[testId] = {}
        qcFeedbackObject[testId].msg = msg
        qcFeedbackObject[testId].msgLite = msgLite
        qcFeedbackObject[testId].testId = testId
      }
    }
    else {
      markTest("display_test_"+testId, true)
      markTestAccepted("id_test_"+testId+"_accepted", null)
    }
  }
}



// // function checkAcceptedTests(objectType) {
//   if (objectType === "lab_sample") {
//     // grab all test related to probability
//     testList = [204,207,302,305,308]
//     for (var i = 0; i < testList.length; i++) {
//       if ($("#id_test_"+testList[i]+"_accepted").val() === "") {
//         markTest("display_test_"+testList[i]+"_accepted",false, "yesNo")
//       }
//       else {
//         markTest("display_test_"+testList[i]+"_accepted",true, "yesNo")
//       }
//     }
//   }
// }


// def run_test_improbable_accepted(object, object_type): # all improbable observations been accepted
//     # ORDER THAT THIS TEST IS RUN IS VERY IMPORTANT: MUST BE AFTER 204 AND 207
//     if object_type === "lab_sample":
//         # START BY DELETING ALL EXISTING SAMPLETEST FOR GIVEN SAMPLE
//         models.FishDetailTest.objects.filter(fish_detail_id=object.id, test_id=208).delete()
//
//         # CREATE BLANK TESTS IN SAMPLETEST
//         # and start off optimistic
//         test = models.FishDetailTest.objects.create(fish_detail_id=object.id,test_id=208,field_name=' global', test_passed=True, scope=1)
//
//         # grab all test related to fish detail
//         fish_detail_tests = models.FishDetailTest.objects.filter(fish_detail_id=object.id)
//         for t in fish_detail_tests: # kEEP IN MIND THIS WILL INCLUDE OTOLITH SAMPLE TESTS
//             if t.accepted === False:
//                 test.test_passed = False
//                 test.save()
//                 break
//
//     elif object_type === "otolith":
//         # START BY DELETING ALL EXISTING SAMPLETEST FOR GIVEN SAMPLE
//         models.FishDetailTest.objects.filter(fish_detail_id=object.id, test_id=211).delete()
//
//         # CREATE BLANK TESTS IN SAMPLETEST
//         # and start off optimistic
//         test = models.FishDetailTest.objects.create(fish_detail_id=object.id,test_id=211,field_name=' global', test_passed=True, scope=2)
//
//         # grab all test related to fish detail
//         fish_detail_tests = models.FishDetailTest.objects.filter(fish_detail_id=object.id)
//         for t in fish_detail_tests: # kEEP IN MIND THIS WILL INCLUDE OTOLITH SAMPLE TESTS
//             if t.accepted === False:
//                 test.test_passed = False
//                 test.save()
//                 break
//
// def run_test_qc_passed(object, object_type): # all quality control tests have been passed
//     # ORDER THAT THIS TEST IS RUN IS VERY IMPORTANT: MUST BE AFTER 202 (mandatory fields), 203 (possible range), 208 (accepted improbable obsverations)
//     if object_type === "lab_sample":
//         # START BY DELETING ALL EXISTING SAMPLETEST FOR GIVEN SAMPLE
//         models.FishDetailTest.objects.filter(fish_detail_id=object.id, test_id=201).delete()
//
//         # CREATE BLANK TESTS IN SAMPLETEST
//         # and start off optimistic
//         test = models.FishDetailTest.objects.create(fish_detail_id=object.id,test_id=201,field_name=' global', test_passed=True, scope=1)
//
//         # grab all test related to fish detail
//         fish_detail_global_tests = models.FishDetailTest.objects.filter(fish_detail_id=object.id).filter(Q(test_id=202) | Q(test_id=203) | Q(test_id=208) )
//
//         for t in fish_detail_global_tests: # Only looking at the tests of interest
//             if t.test_passed === False:
//                 test.test_passed = False
//                 test.save()
//                 break
//
//     elif object_type === "otolith":
//         # START BY DELETING ALL EXISTING SAMPLETEST FOR GIVEN SAMPLE
//         models.FishDetailTest.objects.filter(fish_detail_id=object.id, test_id=200).delete()
//
//         # CREATE BLANK TESTS IN SAMPLETEST
//         # and start off optimistic
//         test = models.FishDetailTest.objects.create(fish_detail_id=object.id,test_id=200,field_name=' global', test_passed=True, scope=2)
//
//         # grab all test related to fish detail
//         fish_detail_global_tests = models.FishDetailTest.objects.filter(fish_detail_id=object.id).filter(Q(test_id=211) | Q(test_id=206) | Q(test_id=210) )
//
//         for t in fish_detail_global_tests: # Only looking at the tests of interest
//             if t.test_passed === False:
//                 test.test_passed = False
//                 test.save()
//                 break
//
//
// def run_data_point_tests(fish_detail, field_name):
//     my_dict = {}
//     stop = False
//     # parse field name
//     if field_name === "fish_length":
//         field = fish_detail.fish_length
//         scope = 1
//     elif field_name === "fish_weight":
//         field = fish_detail.fish_weight
//         scope = 1
//     elif field_name === "gonad_weight":
//         field = fish_detail.gonad_weight
//         scope = 1
//     elif field_name === "annulus_count":
//         field = fish_detail.annulus_count
//         scope = 2
//     else:
//         print("cannot parse field_name")
//         stop = true
//
//     if not stop:
//         # first determine if a test 23 has been accepted
//         try:
//             is_accepted = models.FishDetailTest.objects.filter(fish_detail_id=fish_detail.id, field_name=field_name, test_id=23).first().accepted
//         except Exception as e:
//             print(e)
//             is_accepted = None
//
//         # delete prior test instances
//         models.FishDetailTest.objects.filter(fish_detail_id=fish_detail.id, field_name=field_name).delete()
//
//         # create test instance
//         test_21 = models.FishDetailTest.objects.create(fish_detail_id=fish_detail.id,test_id=21,test_passed=False, field_name=field_name, scope=scope)
//         test_22 = models.FishDetailTest.objects.create(fish_detail_id=fish_detail.id,test_id=22,test_passed=False, field_name=field_name, scope=scope)
//         test_23 = models.FishDetailTest.objects.create(fish_detail_id=fish_detail.id,test_id=23,test_passed=False, field_name=field_name, scope=scope)
//
//         # RUN TESTS
//         if field === None: # no value present; have to use this syntax otherwise a "0" value is excluded
//             pass
//         else: # continue testing
//             test_21.test_passed = True
//             test_21.save()
//             if field < range_dict[field_name]['possible']['min'] or field > range_dict[field_name]['possible']['max']:
//                 pass
//             else:
//                 test_22.test_passed = True
//                 test_22.save()
//                 if field < range_dict[field_name]['probable']['min'] or field > range_dict[field_name]['probable']['max']:
//                     # if the observation was accepted, continue to accept it
//                     if is_accepted === 1:
//                         test_23.accepted = 1
//                     # otherwise, not accepted
//                     else:
//                         test_23.accepted = 0
//
//                 else:
//                     test_23.test_passed = True
//                 test_23.save()
//
//         # if an improbable has not yet been accepted, we have to return a package for the template so that it knows it will have to ask the user to validate observation
//         if test_23.accepted is 0:
//             # my_dict[field_name] = {}
//             my_dict["verbose_name"] = fish_detail._meta.get_field(field_name).verbose_name
//             my_dict["test"] = 23
//             my_dict["msg_lite"] = "Improbable measurement for {}".format(my_dict["verbose_name"])
//             my_dict["msg"] = "{} is outside of the probable range. \\n\\n A value was expected between {} and {}. \\n\\n Are you confident in your measurements? \\n\\n Press [y] for YES or [n] for NO.".format(
//                 my_dict["verbose_name"],
//                 range_dict[field_name]['probable']['min'],
//                 range_dict[field_name]['probable']['max'],
//             )
//         # print(my_dict)
//         return my_dict
