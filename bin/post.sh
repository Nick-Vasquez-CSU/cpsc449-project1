#!/bin/sh

http --verbose POST localhost:5000/wordle/ @"$1"
