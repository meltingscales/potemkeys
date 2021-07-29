package com.example.demo.repository;

import java.util.List;

import com.example.demo.model.Book;
import org.springframework.data.repository.CrudRepository;

public interface BookRepository extends CrudRepository<Book, Long> {
    List<Book> findByTitle(String title);
}