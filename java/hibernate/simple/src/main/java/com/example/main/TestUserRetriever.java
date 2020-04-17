package com.example.main;

import com.example.HibernateUtil;
import com.example.models.Pet;
import com.example.models.User;
import org.hibernate.Query;
import org.hibernate.Session;

import java.util.List;

import static java.lang.System.exit;

/**
 * This class tests retrieval using HQL and Hibernate from the db.
 */
public class TestUserRetriever {

    public static void main(String[] args) {

        Session session = HibernateUtil.getSessionFactory().openSession();

        Query query = session.createQuery("FROM User WHERE username LIKE 'Henry'");

        List<User> results = query.list();

        for (User user : results) {
            System.out.println(user.toString());

            System.out.println("Has these pets:");

            for (Pet pet : user.getPets()) {
                System.out.println(pet.toString());
            }
        }

        session.close();

        exit(0);
    }
}
