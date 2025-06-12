#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "nav2_mppi_controller::mppi_controller" for configuration "Release"
set_property(TARGET nav2_mppi_controller::mppi_controller APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nav2_mppi_controller::mppi_controller PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmppi_controller.so"
  IMPORTED_SONAME_RELEASE "libmppi_controller.so"
  )

list(APPEND _cmake_import_check_targets nav2_mppi_controller::mppi_controller )
list(APPEND _cmake_import_check_files_for_nav2_mppi_controller::mppi_controller "${_IMPORT_PREFIX}/lib/libmppi_controller.so" )

# Import target "nav2_mppi_controller::mppi_critics" for configuration "Release"
set_property(TARGET nav2_mppi_controller::mppi_critics APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(nav2_mppi_controller::mppi_critics PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmppi_critics.so"
  IMPORTED_SONAME_RELEASE "libmppi_critics.so"
  )

list(APPEND _cmake_import_check_targets nav2_mppi_controller::mppi_critics )
list(APPEND _cmake_import_check_files_for_nav2_mppi_controller::mppi_critics "${_IMPORT_PREFIX}/lib/libmppi_critics.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
