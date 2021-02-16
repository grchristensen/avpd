import './InstructorHome.scss'
import React, {useEffect, useState} from "react";
import {useAuth0} from "@auth0/auth0-react";
import {useHistory} from "react-router-dom";
import axios from "axios";
import {NavBar} from "../nav/NavBar";
import {createAssignment, createClassroom, deleteClassroom, getClassrooms} from "../requests";

export function InstructorHome(props) {
  return (
    <div>
      <NavBar firstName={props.userData['first_name']} lastName={props.userData['last_name']}/>
      <Classrooms/>
    </div>
  )
}

function Classrooms() {
  const {getAccessTokenSilently} = useAuth0();
  const [classroomTitles, setClassroomTitles] = useState();

  const history = useHistory()

  useEffect(() => {
    getAccessTokenSilently().then((token) => {
      getClassrooms(token).then((response) => {
        setClassroomTitles(
          response.data.map((data) => <li>
            <button className="classroom-btn" onClick={() => {
              history.push(`/instructor/classrooms/${data['id']}`)
            }}>
              {data['title']}
            </button>
          </li>)
        )
      })
    })
  }, [])

  return (
    <div className="Instructor-Classrooms">
      <div className="classrooms-background">
        <div className="classes-title">
          <p className="classes-text">Classes</p>
        </div>
        <div className="classroom-scroll">
          <ul className="classroom-titles">
            {classroomTitles}
          </ul>
        </div>
        <div className="classroom-create">
          <button onClick={() => {  history.push('/create-classroom')}}>
            Create Classroom
          </button>
        </div>

      </div>
    </div>
  )
}

export function CreateClassroomForm() {
  const [title, setTitle] = useState("");
  const {getAccessTokenSilently} = useAuth0();

  const history = useHistory()

  function handleChange(event) {
    setTitle(event.target.value);
  }

  function handleSubmit(event) {
    getAccessTokenSilently().then((token) => {
      createClassroom(title, token).then((response) => {
        history.push('/')
      }, (error) => console.log(error.response))
    })

    event.preventDefault()
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Title:
        <input type="text" value={title} onChange={handleChange}/>
      </label>
      <input type="submit" value="Submit"/>
    </form>
  )
}