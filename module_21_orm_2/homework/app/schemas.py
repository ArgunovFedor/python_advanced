from marshmallow import Schema, fields


class StudentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    surname = fields.Str()
    phone = fields.Str()
    email = fields.Str()
    average_score = fields.Float()
    scholarship = fields.Bool()


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_name = fields.Str(required=False)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(dump_only=True)
    count = fields.Int(dump_only=True)
    release_date = fields.DateTime(dump_only=True)
    author_id = fields.Int(dump_only=True)


class ReceivingBookSchema(Schema):
    id = fields.Int()
    book_id = fields.Int()
    student_id = fields.Int()
    date_of_issue = fields.DateTime()
    date_of_return = fields.DateTime()
