import database from "../database";
import express, { Router } from "express";

const studentRouter = Router();

type StudentObject = {
  s_no: string;
  register_no: string;
  name: string;
  gpa: string;
  [key: string]: string;
};

studentRouter.post("/students", express.json(), async (req, res) => {
  const semester = parseInt(
    (req.query["semester"] as string | undefined) || ""
  );
  const year = parseInt((req.query["year"] as string | undefined) || "");

  if (Number.isNaN(semester))
    throw new Error("Semester Not Specified or Wrong");
  if (Number.isNaN(year)) throw new Error("Year Not Specified or Wrong");

  const data = req.body as StudentObject[];

  await database.transaction().execute(async (tx) => {
    await tx
      .insertInto("student")
      .values(
        data.map((d) => ({
          student_roll_number: d.register_no,
          student_name: d.name,
        }))
      )
      .onConflict((con) => con.columns(["student_roll_number"]).doNothing())
      .execute();

    const studentsDetails = await tx
      .selectFrom("student")
      .selectAll()
      .where(
        "student.student_roll_number",
        "in",
        data.map((d) => d.register_no)
      )
      .execute();

    tx.insertInto("gpa").values(
      data.map((d) => ({
        student_id: studentsDetails.find(
          (f) => f.student_roll_number == d.register_no
        )!.student_id!,
        student_semester: semester,
        gpa: parseFloat(d.gpa),
      }))
    );

    const subjects = Object.keys(data[0]).filter(
      (f) => !["s_no", "register_no", "name", "gpa"].includes(f)
    );

    tx.insertInto("subjects").values(
      data.map((d) => ({
        subject_id: studentsDetails.find(
          (f) => f.student_roll_number == d.register_no
        )!.student_id!,
        subject_name: ""
      }))
    );
  });
});

export default studentRouter;
