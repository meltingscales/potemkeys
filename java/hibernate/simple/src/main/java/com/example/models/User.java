package com.example.models;

import javax.persistence.*;
import java.util.*;

@Entity
@Table(name = "User", uniqueConstraints = {
        @UniqueConstraint(columnNames = "username")
})
public class User {

    @Id
    @GeneratedValue
    @Column(name = "user_id")
    private int userId;

    @OneToMany(
            cascade = CascadeType.ALL,
            orphanRemoval = true
    )
    private Set<Pet> pets;

    @Column(name = "username")
    private String username;

    @Column(name = "created_by")
    private String createdBy;

    @Column(name = "created_date")
    private Date createdDate;


    public User() {

    }

    @Override
    public String toString() {
        return "User{" +
                "userId=" + userId +
                ", pets=" + "(...)" +
                ", username='" + username + '\'' +
                ", createdBy='" + createdBy + '\'' +
                ", createdDate=" + createdDate +
                '}';
    }

    public User(String username, String createdBy, Date createdDate, int userId, Set<Pet> pets) {
        this.username = username;
        this.createdBy = createdBy;
        this.createdDate = createdDate;
        this.userId = userId;
        this.pets = pets;
    }

    public User(String username, String createdBy, Date createdDate, int userId) {
        this.username = username;
        this.createdBy = createdBy;
        this.createdDate = createdDate;
        this.userId = userId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public Date getCreatedDate() {
        return createdDate;
    }

    public void setCreatedDate(Date createdDate) {
        this.createdDate = createdDate;
    }

    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public Set<Pet> getPets() {
        if (this.pets == null) {
            this.pets = new HashSet<Pet>();
        }
        return pets;
    }

    public void setPets(Set<Pet> pets) {
        this.pets = pets;
    }

    public void addPet(Pet pet) {
        this.getPets().add(pet);
    }
}