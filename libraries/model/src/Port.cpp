////////////////////////////////////////////////////////////////////////////////////////////////////
//
//  Project:  Embedded Machine Learning Library (EMLL)
//  File:     Port.cpp (model)
//  Authors:  Chuck Jacobs
//
////////////////////////////////////////////////////////////////////////////////////////////////////

#include "Port.h"

/// <summary> model namespace </summary>
namespace model
{
    //
    // Specializations of GetTypeCode
    //
    template <>
    Port::PortType Port::GetTypeCode<double>()
    {
        return Port::PortType::Real;
    }

    template <>
    Port::PortType Port::GetTypeCode<int>()
    {
        return Port::PortType::Integer;
    }

    template <>
    Port::PortType Port::GetTypeCode<bool>()
    {
        return Port::PortType::Boolean;
    }

}