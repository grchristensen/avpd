import './App.scss';
import {Route,} from 'react-router-dom';
import {Switch} from 'react-router';
import React from "react";
import {Home} from "./Home";
import About from "./About";
import {MessageHome} from "./Message/MessageHome"
//instructor imports
import {CreateClassroomForm} from "./instructor/InstructorHome";
import {InstructorClassroom, CreateAssignmentForm} from "./instructor/InstructorClassroom";
import {InstructorNameList} from "./instructor/InstructorNameList";
import {InstructorAssignment, UpdateAssignmentForm} from "./instructor/InstructorAssignment";
//student Inports
import {JoinClassroomForm} from "./student/StudentHome"
import {StudentAssignment} from "./student/StudentAssignment.js"
import {PostSubmit} from "./student/PostSubmit.js"

function App() {
  return (
    <Main/>
  );
}

function Main() {
  return (
    <Switch>
      <Route exact path="/" component={Home}/>
      <Route exact path="/about" component={About}/>
      {/* forms instructor*/}
      <Route exact path="/create-classroom" component={CreateClassroomForm}/>
      <Route exact path="/create-assignment" component={CreateAssignmentForm}/>
      <Route exact path="/update-assignment" component={UpdateAssignmentForm}/>
      <Route exact path="/join-classroom" component={JoinClassroomForm}/>
      {/*intructor menu*/}
      <Route exact path="/instructor/classrooms/:id" component={InstructorClassroom}/>
      <Route exact path="/instructor/classrooms/:classroomID/assignments/:id" component={InstructorAssignment}/>
      <Route exact path="/instructor/classrooms/:id/students" component={InstructorNameList}/>
      {/*Student menu*/}
      <Route exact path="/student/classrooms/:classroomID/assignments/:id" component={StudentAssignment}/>
      <Route exact path="/student/classrooms/:classroomID/assignments/:id/submit" component={PostSubmit}/>
    </Switch>
  )
}

export default App;