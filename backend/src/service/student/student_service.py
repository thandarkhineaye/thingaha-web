import traceback
from typing import List, Dict, Any, Optional

from sqlalchemy.exc import SQLAlchemyError

from common.data_schema import student_schema
from common.error import SQLCustomError, RequestDataEmpty, ValidateFail
from models.student import StudentModel
from service.service import Service


class StudentService(Service):
    """
    student service class for CRUD actions
    define specific params for student service in StudentService Class
    """
    def __init__(self, logger=None) -> None:
        super().__init__(logger)

    @staticmethod
    def __return_student_list(query: list) -> List:
        """
        return list by query
        :param query:
        :return:
        """
        return [student.student_dict() for student in query]

    def get_all_student_address(self, page: int = 1) -> (List[Dict], int):
        """
        get all school address for get all address API
        :params page integer
        :return
        """
        try:
            self.logger.info("Get all student address list")
            students_address = StudentModel.get_all_student_address(page)
            return [address.address_type_dict(student) for address, student in students_address.items], students_address.total
        except SQLAlchemyError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="GET student address SQL ERROR")

    def get_all_students(self, page: int = 1) -> (List, Any):
        """
        get all student
        :params page
        :return: student list of dict
        """
        try:
            self.logger.info("Get all students list")
            students = StudentModel.get_all_students(page)
            return self.__return_student_list(students.items), students.total
        except SQLAlchemyError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="GET Student SQL ERROR")

    def get_student_by_id(self, student_id: int) -> Optional[Dict]:
        """
        get student info by id
        :param student_id:
        :return: student list of dict
        """
        try:
            self.logger.info("Get student info by student_id:{}".format(student_id))
            student = StudentModel.get_student_by_id(student_id)
            if not student:
                raise SQLCustomError(description="No data for requested student id: {}".format(student_id))
            return student.student_dict()
        except SQLAlchemyError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="GET student by ID SQL ERROR")

    def create_student(self, data: Dict[str, Any]) -> int:
        """
        create school records
        :param data:
        :return: created student id
        """
        if not data:
            raise RequestDataEmpty("Student data is empty")
        if not self.input_validate.validate_json(data, student_schema):
            self.logger.error("All student field input must be required.")
            raise ValidateFail("Student validation fail")
        try:
            return StudentModel.create_student(StudentModel(
                name=data["name"],
                deactivated_at=data["deactivated_at"],
                birth_date=data["birth_date"],
                father_name=data["father_name"],
                mother_name=data["mother_name"],
                parents_occupation=data["parents_occupation"],
                photo=data["photo"],
                address_id=data["address_id"]))
        except SQLAlchemyError as error:
            self.logger.error("Student create fail. name %s, error %s, format: %s ", data["name"], error, traceback.format_exc())
            raise SQLCustomError("Student create fail")

    def delete_student_by_id(self, student_id: int) -> bool:
        """
        delete student by id
        :param student_id:
        :return:
        """
        try:
            self.logger.info("Delete student info by student_id:{}".format(student_id))
            return StudentModel.delete_student(student_id)
        except SQLAlchemyError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="Delete student by ID SQL ERROR")

    def update_student_by_id(self, student_id: int, data: Dict) -> bool:
        """
        put student by id
        :param student_id:
        :param data:
        :return:
        """
        if not data:
            raise RequestDataEmpty("Student data is empty")
        if not self.input_validate.validate_json(data, student_schema):
            self.logger.error("All student field input must be required.")
            raise ValidateFail("Student update validation fail")
        try:
            self.logger.info("Update student info by student_id:{}".format(student_id))
            return StudentModel.update_student(student_id, StudentModel(
                name=data["name"],
                deactivated_at=data["deactivated_at"],
                birth_date=data["birth_date"],
                father_name=data["father_name"],
                mother_name=data["mother_name"],
                parents_occupation=data["parents_occupation"],
                photo=data["photo"],
                address_id=data["address_id"]))
        except SQLAlchemyError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="Update student by ID SQL ERROR")
        except SQLCustomError as error:
            self.logger.error("Error: {}".format(error))
            raise SQLCustomError(description="No record for requested student")
