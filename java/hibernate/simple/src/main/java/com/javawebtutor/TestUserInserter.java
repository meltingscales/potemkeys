package com.javawebtutor;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;

import org.hibernate.Session;

/***
 * This class inserts test Users.
 */
public class TestUserInserter {
    public static List<User> users = new ArrayList<User>(
            Arrays.<User>asList(
                    new User("Dani", "Google", new Date(), 1),
                    new User("Henry", "U.S. Bank", new Date(), 2)
            )
    );


    public static void main(String[] args) {
        Session session = HibernateUtil.getSessionFactory().openSession();

        for (User user : users) {
            session.beginTransaction();

            session.save(user);
            session.getTransaction().commit();
        }

        session.close();
    }

}