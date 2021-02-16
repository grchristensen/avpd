import axios from "axios";
import {authenticateRequest, serverUrl} from "./utils";

export async function getUserData(token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/user`, requestConfig)
}

//instructor
export async function getClassrooms(token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/instructor/classrooms`, requestConfig)
}

export async function createClassroom(title, token) {
  let requestConfig = {}

  const data = {
    'title': title
  }

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.post(`${serverUrl()}/instructor/classrooms`, data, requestConfig)
}

export async function deleteClassroom(classroomID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.delete(`${serverUrl()}/instructor/classrooms/${classroomID}`, requestConfig)
}

export async function createAssignment(classroomID, title, description, dueDate, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  const data = {
    'title': title,
    'description': description,
    'due_date': dueDate,
  }

  return axios.post(`${serverUrl()}/instructor/classrooms/${classroomID}/assignments`, data, requestConfig)
}

export async function getSubmission(classroomID, assignmentID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions/${id}`,
    requestConfig)
}

export async function getSubmissionReport(classroomID, assignmentID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments/${assignmentID}/submissions/${id}/report`,
    requestConfig)
}

export async function getClassroomStudent(classroomID, id, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/classrooms/${classroomID}/students/${id}`,
    requestConfig)
}

export async function getInstructorAssignments(classroomID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classroomID}/assignments`,
    requestConfig)
}

export async function viewInstructorAssignment(classNumber, assignmentID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/instructor/classrooms/${classNumber}/assignments/${assignmentID}`, requestConfig
  )
}

//student functions
export async function getAssignments(token, classNumber) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(`${serverUrl()}/student/classrooms/${classNumber}/assignments`, requestConfig)
}

export async function viewAssignment(classNumber, assignmentID, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.get(
    `${serverUrl()}/student/classrooms/${classNumber}/assignments/${assignmentID}`, requestConfig
  )
}

export async function SubmitEssay(classNumber, assignmentID, file, token) {
  let requestConfig = {}

  requestConfig = await authenticateRequest(requestConfig, token)

  return axios.post(
    `${serverUrl()}/student/classrooms/${classNumber}/assignments/${assignmentID}/submissions`, file, requestConfig
  )
}