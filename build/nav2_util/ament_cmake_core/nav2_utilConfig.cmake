# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_nav2_util_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED nav2_util_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(nav2_util_FOUND FALSE)
  elseif(NOT nav2_util_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(nav2_util_FOUND FALSE)
  endif()
  return()
endif()
set(_nav2_util_CONFIG_INCLUDED TRUE)

# output package information
if(NOT nav2_util_FIND_QUIETLY)
  message(STATUS "Found nav2_util: 1.3.7 (${nav2_util_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'nav2_util' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT nav2_util_DEPRECATED_QUIET)
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(nav2_util_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "ament_cmake_export_include_directories-extras.cmake;ament_cmake_export_libraries-extras.cmake;ament_cmake_export_dependencies-extras.cmake;ament_cmake_export_targets-extras.cmake")
foreach(_extra ${_extras})
  include("${nav2_util_DIR}/${_extra}")
endforeach()
