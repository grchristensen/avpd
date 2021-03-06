from notebooks.feature_extractors.pospca_extractor import POSPCAExtractor


class TestPOSPCAExtractor:
    def test_entry_point(self):
        extractor = POSPCAExtractor(4, 10)

        result = extractor(
            "A prototype for a plagiarism detection system is created and evaluated. The system will determine if an essay submitted by a student is their own work, based on statistical patterns in previous essays, such as average sentence length or vocabulary usage. Instructors will be able to assess how similar a student’s submitted work is to their previous work. Students will be able to keep their account and essay history for future classes, and the system will become more accurate as the student submits more essays. The server-side application is broken down into modular components that handle different types of requests. Components that handle the comparison of student work are separated from components that handle the management of classrooms and assignments."
            + "Our web application would act as a database for submitting and storing essays and use that data to determine if a student is creating original essays via content pattern recognition. It will do this by tracking past essays as samples to create a profile of student users. The application would determine relevant features about the past assignments and use these features to determine if a new assignment is an anomaly. Instructors would be able to submit essays and then compare them to that student's essay profile. Students would also be able to submit essays and look at all their essays from different classes. This would help increase the accuracy of the pattern recognition software. If a score has an abnormality, the instructor would be notified for personal review for plagiarism."
            + "Our system was designed to separate components that handle the comparison of essays to a student’s previous work from components that handle the management of users. These user management components are further separated into components that handle students, components that handle instructors, and components that handle the virtual classrooms that connect students and instructors. In addition there are components that handle social features such as student to instructor messaging. The separation of components this way allows the members of our team, who have different skill sets, to work on the aspects of the project that they can excel at. With the different program units defined, the interaction between these units and the actual data structures that compose the units can be determined."
        )

        pass
