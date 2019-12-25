package com.example.main;

import java.util.*;

import com.example.HibernateUtil;
import com.example.models.Pet;
import com.example.models.PetType;
import com.example.models.User;
import org.hibernate.Session;

import static java.lang.System.exit;

/***
 * This class inserts test Users.
 */
public class TestUserInserter {

    public static List<User> users = new ArrayList<User>();

    static {
        users.add(new User("Dani", "Google", new Date(), 0));

        User henry = new User("Henry", "U.S. Bank", new Date(), 0);

        henry.addPet(new Pet("Anthony", 0, PetType.CAT));
        henry.addPet(new Pet("Jackson", 0, PetType.CAT));
        henry.addPet(new Pet("Rufus", 0, PetType.DOG));
        henry.addPet(new Pet("Todd", 0, PetType.DOG));

        users.add(henry);
    }

    public static void main(String[] args) {
        Session session = HibernateUtil.getSessionFactory().openSession();

        for (User user : users) {
            session.beginTransaction();

            session.save(user);
            session.getTransaction().commit();
        }

        session.close();

        exit(0);
    }

}