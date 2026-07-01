// Task 60
db = db.getSiblingDB("college_nosql");

// Task 61
db.createCollection("feedback")

// Task 62 & 63
db.feedback.insertMany([
{
    student_id: 1,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Excellent teaching. Would recommend.",
    tags: ["challenging", "well-structured", "good-examples"],
    submitted_at: ISODate("2022-11-30T10:15:00Z"),
    attachments: [
        {
            filename: "notes.pdf",
            size_kb: 240
        }
    ]
},
{
    student_id: 2,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Very informative.",
    tags: ["challenging", "interactive"],
    submitted_at: ISODate("2022-11-28T09:30:00Z"),
    attachments: [
        {
            filename: "lab.pdf",
            size_kb: 180
        }
    ]
},
{
    student_id: 5,
    course_code: "CS101",
    semester: "2022-ODD",
    rating: 5,
    comments: "Loved the examples.",
    tags: ["challenging", "good-examples"],
    submitted_at: ISODate("2022-11-25T11:45:00Z"),
    attachments: [
        {
            filename: "assignment.pdf",
            size_kb: 210
        }
    ]
},
{
    student_id: 1,
    course_code: "CS102",
    semester: "2022-EVEN",
    rating: 4,
    comments: "Database concepts are clear.",
    tags: ["sql", "practical"],
    submitted_at: ISODate("2023-04-15T10:00:00Z"),
    attachments: [
        {
            filename: "database.pdf",
            size_kb: 200
        }
    ]
},
{
    student_id: 5,
    course_code: "CS102",
    semester: "2022-EVEN",
    rating: 2,
    comments: "Need more practical sessions.",
    tags: ["sql", "difficult"],
    submitted_at: ISODate("2023-04-18T09:15:00Z"),
    attachments: [
        {
            filename: "review.pdf",
            size_kb: 120
        }
    ]
},
{
    student_id: 8,
    course_code: "CS103",
    semester: "2022-ODD",
    rating: 3,
    comments: "Average experience.",
    tags: ["oop", "coding"],
    submitted_at: ISODate("2022-11-20T08:20:00Z"),
    attachments: [
        {
            filename: "program.pdf",
            size_kb: 140
        }
    ]
},
{
    student_id: 3,
    course_code: "EC101",
    semester: "2021-EVEN",
    rating: 5,
    comments: "Excellent faculty.",
    tags: ["electronics", "practical"],
    submitted_at: ISODate("2021-12-01T09:00:00Z"),
    attachments: [
        {
            filename: "circuit.pdf",
            size_kb: 160
        }
    ]
},
{
    student_id: 6,
    course_code: "EC101",
    semester: "2022-ODD",
    rating: 4,
    comments: "Interesting labs.",
    tags: ["electronics", "challenging"],
    submitted_at: ISODate("2022-11-18T10:45:00Z"),
    attachments: [
        {
            filename: "labmanual.pdf",
            size_kb: 150
        }
    ]
},
{
    student_id: 4,
    course_code: "ME101",
    semester: "2022-ODD",
    rating: 2,
    comments: "Needs improvement.",
    tags: ["mechanical", "hard"],
    submitted_at: ISODate("2022-11-15T12:30:00Z"),
    attachments: [
        {
            filename: "thermo.pdf",
            size_kb: 175
        }
    ]
},
{
    student_id: 7,
    course_code: "ME101",
    semester: "2023-ODD",
    rating: 5,
    comments: "Very useful course.",
    tags: ["mechanical", "interesting"],
    submitted_at: ISODate("2023-11-15T10:00:00Z")
}
])

// Task 64
db.feedback.countDocuments()

// ==========================
// Task 65
// ==========================
db.feedback.find({
    rating: 5
})

// ==========================
// Task 66
// ==========================
db.feedback.find({
    course_code: "CS101",
    tags: "challenging"
})

// ==========================
// Task 67
// ==========================
db.feedback.find(
{},
{
    _id: 0,
    student_id: 1,
    course_code: 1,
    rating: 1
}
)

// ==========================
// Task 68
// ==========================
db.feedback.updateMany(
{
    rating: { $lt: 3 }
},
{
    $set: {
        needs_review: true
    }
}
)

// ==========================
// Task 69
// ==========================
db.feedback.updateMany(
{
    needs_review: true
},
{
    $push: {
        tags: "reviewed"
    }
}
)

// ==========================
// Task 70
// ==========================
db.feedback.deleteMany({
    semester: "2021-EVEN"
})

// ==========================
// Task 71
// ==========================
db.feedback.aggregate([
{
    $match: {
        semester: "2022-ODD"
    }
},
{
    $group: {
        _id: "$course_code",
        avg_rating: {
            $avg: "$rating"
        },
        total_feedback: {
            $sum: 1
        }
    }
},
{
    $sort: {
        avg_rating: -1
    }
}
])

// ==========================
// Task 72
// ==========================
db.feedback.aggregate([
{
    $match: {
        semester: "2022-ODD"
    }
},
{
    $group: {
        _id: "$course_code",
        avg_rating: {
            $avg: "$rating"
        },
        total_feedback: {
            $sum: 1
        }
    }
},
{
    $project: {
        _id: 0,
        course_code: "$_id",
        average_rating: {
            $round: [
                "$avg_rating",
                1
            ]
        },
        total_feedback: 1
    }
},
{
    $sort: {
        average_rating: -1
    }
}
])

// ==========================
// Task 73
// ==========================
db.feedback.aggregate([
{
    $unwind: "$tags"
},
{
    $group: {
        _id: "$tags",
        count: {
            $sum: 1
        }
    }
},
{
    $sort: {
        count: -1
    }
}
])

// ==========================
// Task 74
// ==========================
db.feedback.createIndex({
    course_code: 1
})

db.feedback.find({
    course_code: "CS101"
}).explain("executionStats")